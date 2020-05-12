#!/bin/sh -e
mkdir -p nomenklatura/static/vendor
mkdir -p /var/log/nomenklatura
python manage.py createdb

# nginx settings
# sets FORWARDED_ALLOW_IPS to 127.0.0.1 if not set
# FORWARDED_ALLOW_IPS="${FORWARDED_ALLOW_IPS:-127.0.0.1}"

if [[ "$*" == "worker" ]];then
    exec celery -A nomenklatura.importer worker \
        --concurrency=4 \
        --max-tasks-per-child=1 \
        --loglevel=${CELERY_LOGLEVEL} \
        --autoscale=${CELERY_AUTOSCALE} \
        --pidfile /var/run/celery.pid

elif [[ "$*" == "nomenklatura" ]];then
    exec gunicorn manage:app \
        --bind 0.0.0.0:8000 \
        --workers 4 \
        --access-logfile - \
        --log-level debug
else
    exec "$@"
fi