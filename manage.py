from normality import normalize
from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from nomenklatura.core import db
from nomenklatura.model import Entity
from nomenklatura.model import Dataset
from nomenklatura.views import app
from nomenklatura.assets import assets

manager = Manager(app)
manager.add_command('assets', ManageAssets(assets))


@manager.command
def createdb():
    """ Make the database. """
    db.engine.execute("CREATE EXTENSION IF NOT EXISTS hstore;")
    db.engine.execute("CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;")
    db.create_all()


@manager.command
def flush(dataset):
    ds = Dataset.by_name(dataset)
    for alias in Alias.all_unmatched(ds):
        db.session.delete(alias)
    db.session.commit()


@manager.option('-h', '--host', dest='host', default='127.0.0.1')
@manager.option('-p', '--port', dest='port', type=int, default=5000)
@manager.option('-w', '--workers', dest='workers', type=int, default=8)
def gunicorn(host, port, workers):
    """Start the Server with Gunicorn"""
    from gunicorn.app.base import Application

    class FlaskApplication(Application):
        def init(self, parser, opts, args):
            return {
                'bind': '{0}:{1}'.format(host, port),
                'workers': workers
            }

        def load(self):
            return app

    application = FlaskApplication()
    return application.run()


if __name__ == '__main__':
    manager.run()
