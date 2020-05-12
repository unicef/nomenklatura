## Nomenklatura

Nomenklatura de-duplicates and integrates different names for entities - people, organisations or public bodies - to help you clean up messy data and to find links between different datasets.

The service will create references for all entities mentioned in a source dataset. It then helps you to define which of these entities are duplicates and what the canonical name for a given entity should be. This information is available in data cleaning tools like OpenRefine or in custom data processing scripts, so that you can automatically apply existing mappings in the future. 

The focus of nomenklatura is on data integration, it does not provide further functionality with regards to the people and organisations that it helps to keep track of. 

### About this fork
This is a fork of [pudo/nomenklatura](https://github.com/pudo/nomenklatura). OpenNames.org, a public hosted instance of nomenklatura got [recently shut down](https://github.com/pudo/nomenklatura/wiki/OpenNames.org-Shutdown-Notice) because the project has taken a different direction. This fork tries to maintain a compatible version of nomenklatura thats usable as a plug-in replacement.

A docker image is available as `unicef/nomenklatura` in the [docker index](https://hub.docker.com/r/unicef/nomenklatura/).


System Requirements
------------------------------------
* postgres
* virtualenvwrapper


Quick Installation
------------------------------------

    pipenv install
    npm install  --prefix ./nomenklatura/static/vendor

    psql -c 'CREATE DATABASE nomenklatura;' -U postgres

    python manage.py createdb
    python manage.py runserver


### Usage

If you want to deploy your own Nomenklatura instance, use the [`unicef/nomenklatura` docker container](https://hub.docker.com/r/unicef/nomenklatura/):

```
docker-compose up
```

Required environment variables:
```
DATABASE_URL: postgres://username:password@databasehost/nomenklatura
SECRET_KEY: something_unique_and_secret_here # used for the session cookie
```

#### Authentication
[Register a new OAuth application](https://github.com/settings/developers) on github with the following parameters:

* __Homepage URL__: URL to your nomenklatura instance
* __Authorization Callback URL__: https://your.nomenklatura.example/api/2/sessions/callback

Then add these environment variables:
```
GITHUB_CLIENT_ID: your_client_id_from_github
GITHUB_CLIENT_SECRET: your_client_secret_from_github
```

### Contact, contributions etc.

nomenklatura is developed with generous support by [Knight-Mozilla OpenNews](http://opennews.org) and the [Open Knowledge Foundation Labs](http://okfnlabs.org). The codebase is licensed under the terms of an MIT license (see LICENSE.md).

We're keen for any contributions, bug fixes and feature suggestions, please use the GitHub issue tracker for this repository. 

