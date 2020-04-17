DEBUG = True
SECRET_KEY = 'no'
APP_NAME = 'nomenklatura'
SQLALCHEMY_DATABASE_URI = 'sqlite:///master.sqlite3'
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'

ALLOWED_EXTENSIONS = set(['csv', 'tsv', 'ods', 'xls', 'xlsx', 'txt'])

SIGNUP_DISABLED = False
DATASET_CREATION_DISABLED = False

SYSTEM_MESSAGE = ''
