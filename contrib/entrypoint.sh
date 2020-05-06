#!/bin/sh -e
mkdir -p nomenklatura/static/vendor
mkdir -p /var/log/nomenklatura
python manage.py createdb

# sets FORWARDED_ALLOW_IPS to 127.0.0.1 if not set
# FORWARDED_ALLOW_IPS="${FORWARDED_ALLOW_IPS:-127.0.0.1}"

exec gunicorn nomenklatura.manage:app \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --access-logfile - \
    --log-level debug
