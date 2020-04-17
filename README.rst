Nomenklatura
===================================


System Requirements
------------------------------------
* postgres
* virtualenvwrapper


Quick Installation
------------------------------------
::

    pipenv install
    bower install
    sudo npm install -g less uglify-js

    psql -c 'CREATE DATABASE nomenklatura;' -U postgres

    create settings file (settings.py)


    python manage.py createdb
    python manage.py gunicorn



    NOMENKLATURA_SETTINGS='settings.py' python manage.py gunicorn\ No newline at end of file