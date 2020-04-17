import os

from apikit import jsonify
from flask import render_template, request, session
from formencode import Invalid
from werkzeug.exceptions import Unauthorized

from nomenklatura.core import app
from nomenklatura.model import Account
from nomenklatura.views.datasets import section as datasets
from nomenklatura.views.entities import section as entities
from nomenklatura.views.matching import section as matching
from nomenklatura.views.reconcile import section as reconcile
from nomenklatura.views.sessions import section as sessions
from nomenklatura.views.upload import section as upload


@app.before_request
def check_auth():
    api_key = request.headers.get('Authorization') \
        or request.args.get('api_key')
    if session.get('id'):
        request.account = Account.by_github_id(session.get('id'))
        if request.account is None:
            del session['id']
            raise Unauthorized()
    elif api_key is not None:
        request.account = Account.by_api_key(api_key)
        if request.account is None:
            raise Unauthorized()
    else:
        request.account = None


@app.errorhandler(Invalid)
def handle_invalid(exc):
    body = {
        'status': 400,
        'name': 'Invalid Data',
        'description': str(exc),
        'errors': exc.unpack_errors()
    }
    return jsonify(body, status=400)


app.register_blueprint(upload, url_prefix='/api/2')
app.register_blueprint(reconcile, url_prefix='/api/2')
app.register_blueprint(sessions, url_prefix='/api/2')
app.register_blueprint(datasets, url_prefix='/api/2')
app.register_blueprint(entities, url_prefix='/api/2')
app.register_blueprint(matching, url_prefix='/api/2')


def angular_templates():
    if app.config.get('ASSETS_DEBUG'):
        return
    partials_dir = os.path.join(app.static_folder, 'templates')
    for (root, dirs, files) in os.walk(partials_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'rb') as fh:
                yield ('/static/templates/%s' % file_path[len(partials_dir) + 1:],
                       fh.read().decode('utf-8'))


@app.route('/entities')
@app.route('/entities/<path:id>')
@app.route('/datasets')
@app.route('/datasets/<path:id>')
@app.route('/profile')
@app.route('/docs/<path:id>')
@app.route('/')
def index(**kw):
    return render_template('app.html', angular_templates=angular_templates(), system_message=app.config.get('SYSTEM_MESSAGE'))
