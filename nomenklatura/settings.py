import os

DEBUG = True
SECRET_KEY = 'no'
APP_NAME = 'nomenklatura'

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///master.sqlite3')
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'

ALLOWED_EXTENSIONS = set(['csv', 'tsv', 'ods', 'xls', 'xlsx', 'txt'])

SIGNUP_DISABLED = False
DATASET_CREATION_DISABLED = False

SYSTEM_MESSAGE = ''


LOG_FOLDER = os.getenv('LOG_FOLDER', '/var/log/nomenklatura')
GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')
