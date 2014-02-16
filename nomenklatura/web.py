import os

from flask import Blueprint, render_template, make_response
from flask import redirect

from grano.core import app


base = Blueprint('nomenklatura', __name__, static_folder='static', template_folder='templates')


def angular_templates():
    #if app.config.get('ASSETS_DEBUG'):
    #    return
    partials_dir = os.path.join(base.static_folder, 'templates')
    for (root, dirs, files) in os.walk(partials_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'rb') as fh:
                yield ('/static/templates/%s' % file_path[len(partials_dir)+1:],
                       fh.read().decode('utf-8'))


@base.route('/entities')
@base.route('/entities/<path:id>')
@base.route('/datasets')
@base.route('/datasets/<path:id>')
@base.route('/profile')
@base.route('/docs/<path:id>')
@base.route('/')
def index(**kw):
    return render_template('app.html', angular_templates=angular_templates())


app.register_blueprint(base)

