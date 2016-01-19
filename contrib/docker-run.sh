#!/bin/bash

mkdir -p nomenklatura/static/vendor
bower install --allow-root --config.interactive=false
python nomenklatura/manage.py createdb
# python nomenklatura/manage.py assets build

# sets FORWARDED_ALLOW_IPS to 127.0.0.1 if not set
FORWARDED_ALLOW_IPS="${FORWARDED_ALLOW_IPS:-127.0.0.1}"

exec gunicorn nomenklatura.manage:app \
    --bind 0.0.0.0:8080 \
    --workers 4 \
    --access-logfile - \
    --forwarded-allow-ips $FORWARDED_ALLOW_IPS
# for debugging: add \ to the previous line and
#   --log-level debug