import logging

import requests
from apikit import jsonify
from flask import Blueprint, redirect, request, session, url_for
from werkzeug.exceptions import Forbidden

from nomenklatura import authz
from nomenklatura.core import app, db, github
from nomenklatura.model import Account, Dataset

section = Blueprint('sessions', __name__)


@section.route('/sessions')
def status():
    return jsonify({
        'logged_in': authz.logged_in(),
        'api_key': request.account.api_key if authz.logged_in() else None,
        'account': request.account,
        'base_url': url_for('index', _external=True)
    })


@section.route('/sessions/authz')
def get_authz():
    permissions = {}
    dataset_name = request.args.get('dataset')
    if dataset_name is not None:
        dataset = Dataset.find(dataset_name)
        permissions[dataset_name] = {
            'view': True,
            'edit': authz.dataset_edit(dataset),
            'manage': authz.dataset_manage(dataset)
        }
    return jsonify(permissions)


@section.route('/sessions/login')
def login():
    callback = url_for('sessions.authorized', _external=True)
    return github.authorize(callback=callback)


@section.route('/sessions/logout')
def logout():
    logging.info(authz.require(authz.logged_in()))
    session.clear()
    return redirect('/')


@section.route('/sessions/callback')
@github.authorized_handler
def authorized(resp):
    if 'access_token' not in resp:
        return redirect(url_for('index', _external=True))
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    res = requests.get('https://api.github.com/user?access_token=%s' % access_token,
                       verify=False)
    data = res.json()
    for k, v in data.items():
        session[k] = v
    account = Account.by_github_id(data.get('id'))
    if account is None:
        if app.config.get('SIGNUP_DISABLED'):
            raise Forbidden("Sorry, account creation is disabled")
        account = Account.create(data)
        db.session.commit()
    return redirect('/')
