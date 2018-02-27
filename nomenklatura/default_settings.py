DEBUG = False
APP_NAME = 'nomenklatura'

CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'

ALLOWED_EXTENSIONS = set(['csv', 'tsv', 'ods', 'xls', 'xlsx', 'txt'])

SIGNUP_DISABLED = False
