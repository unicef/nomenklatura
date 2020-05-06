import os

APP_NAME = os.environ.get('APP_NAME', 'nomenklatura')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///master.sqlite3')
DEBUG = os.environ.get('DEBUG', True)
SECRET_KEY = os.environ.get('SECRET_KEY', 'secret_key')

CELERY_BROKER = os.environ.get('CLOUDAMQP_URL')
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'amqp://guest:guest@localhost:5672//')

ALLOWED_EXTENSIONS = set(['csv', 'tsv', 'ods', 'xls', 'xlsx', 'txt'])
LOG_FOLDER = os.getenv('LOG_FOLDER', '/var/log/nomenklatura')

SIGNUP_DISABLED = os.getenv('SIGNUP_DISABLED', False)
DATASET_CREATION_DISABLED = os.getenv('DATASET_CREATION_DISABLED', False)

SYSTEM_MESSAGE = os.environ.get('SYSTEM_MESSAGE', '')
MEMCACHE_HOST = os.environ.get('MEMCACHIER_SERVERS')

GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')
SENTRY_DSN = os.getenv('SENTRY_DSN')

S3_BUCKET = os.environ.get('S3_BUCKET', 'nomenklatura')
S3_ACCESS_KEY = os.environ.get('S3_ACCESS_KEY')
S3_SECRET_KEY = os.environ.get('S3_SECRET_KEY')
