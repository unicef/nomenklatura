import logging
from logging.handlers import RotatingFileHandler

import sentry_sdk
from celery import Celery
from flask import Flask, url_for as _url_for
from flask_assets import Environment
from flask_oauthlib.client import OAuth
from flask_sqlalchemy import SQLAlchemy
from kombu import Exchange, Queue

from nomenklatura import settings

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object(settings)
app.config.from_envvar('NOMENKLATURA_SETTINGS', silent=True)
app_name = app.config.get('APP_NAME')

log_folder = app.config.get('LOG_FOLDER')
file_handler = RotatingFileHandler('{}/errors.log'.format(log_folder),
                                   maxBytes=1024 * 1024 * 100,
                                   backupCount=20)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

db = SQLAlchemy(app)
assets = Environment(app)

celery = Celery(app_name, broker=app.config['CELERY_BROKER_URL'])
queue_name = app_name + '_q'
app.config['CELERY_DEFAULT_QUEUE'] = queue_name
app.config['CELERY_QUEUES'] = (
    Queue(queue_name, Exchange(queue_name), routing_key=queue_name),
)

celery.config_from_object(app.config)

oauth = OAuth()
github = oauth.remote_app(
    'github',
    base_url='https://github.com/login/oauth/',
    authorize_url='https://github.com/login/oauth/authorize',
    request_token_url=None,
    access_token_url='https://github.com/login/oauth/access_token',
    consumer_key=app.config.get('GITHUB_CLIENT_ID'),
    consumer_secret=app.config.get('GITHUB_CLIENT_SECRET'))


def url_for(*a, **kw):
    try:
        kw['_external'] = True
        return _url_for(*a, **kw)
    except RuntimeError:
        return None


if app.debug is not True and app.config['SENTRY_DSN']:
    sentry_sdk.init(dsn=app.config['SENTRY_DSN'])
