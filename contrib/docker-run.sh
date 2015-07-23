#!/bin/bash

mkdir -p nomenklatura/static/vendor
bower install --allow-root --config.interactive=false
python nomenklatura/manage.py createdb
# python nomenklatura/manage.py assets build
exec gunicorn nomenklatura.manage:app \
    --bind 0.0.0.0:8080 \
    --workers 4 \
    --access-logfile -
# for debugging: add \ to the previous line and
#   --log-level debug