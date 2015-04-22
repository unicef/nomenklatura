#!/bin/bash

mkdir -p nomenklatura/static/vendor
bower install --allow-root --config.interactive=false
python nomenklatura/manage.py createdb
python nomenklatura/manage.py runserver -p 8080 -h 0.0.0.0
