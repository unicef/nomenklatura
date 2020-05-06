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
    sudo npm install -g less uglify-js bower
    bower install

    psql -c 'CREATE DATABASE nomenklatura;' -U postgres

    create settings file (settings.py)


    python manage.py createdb
    python manage.py gunicorn



    python manage.py gunicorn
