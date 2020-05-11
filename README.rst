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
    npm install  --prefix ./nomenklatura/static/vendor

    psql -c 'CREATE DATABASE nomenklatura;' -U postgres

    create settings file (settings.py)


    python manage.py createdb
    python manage.py runserver
