import logging

from apikit import jsonify
from flask import Blueprint, redirect, request, session, url_for
from werkzeug.exceptions import Forbidden

from nomenklatura import authz
from nomenklatura.core import app, db, oauth
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
    redirect_uri = url_for('sessions.authorize', _external=True)
    return oauth.github.authorize_redirect(redirect_uri)


@section.route('/sessions/logout')
def logout():
    logging.info(authz.require(authz.logged_in()))
    session.clear()
    return redirect('/')


@section.route('/authorize')
def authorize():
    token = oauth.github.authorize_access_token()
    resp = oauth.github.get('user', token=token)
    profile = resp.json()
    for k, v in profile.items():
        session[k] = v
    account = Account.by_github_id(profile.get('id'))
    if account is None:
        if app.config.get('SIGNUP_DISABLED'):
            raise Forbidden("Sorry, account creation is disabled")
        Account.create(profile)
        db.session.commit()

    return redirect('/')
