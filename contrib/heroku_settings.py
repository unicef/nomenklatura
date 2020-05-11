import os


def bool_env(val):
    """Replaces string based environment values with Python booleans"""
    return True if os.environ.get(val, 'False').lower() == 'true' else False


# DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', os.environ.get('SHARED_DATABASE_URL'))

APP_NAME = os.environ.get('APP_NAME', 'nomenklatura')

GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')

MEMCACHE_HOST = os.environ.get('MEMCACHIER_SERVERS')

S3_BUCKET = os.environ.get('S3_BUCKET', 'nomenklatura')
S3_ACCESS_KEY = os.environ.get('S3_ACCESS_KEY')
S3_SECRET_KEY = os.environ.get('S3_SECRET_KEY')

CELERY_BROKER = os.environ.get('CLOUDAMQP_URL')

SIGNUP_DISABLED = bool_env('SIGNUP_DISABLED')
DATASET_CREATION_DISABLED = bool_env('DATASET_CREATION_DISABLED')
LOG_FOLDER = os.environ.get('LOG_FOLDER')

SYSTEM_MESSAGE = os.environ.get('SYSTEM_MESSAGE')