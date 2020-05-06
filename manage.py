import logging

from flask_assets import ManageAssets
from flask_script import Manager
from sqlalchemy.sql import Alias

from nomenklatura.assets import assets
from nomenklatura.core import db
from nomenklatura.model import Dataset
from nomenklatura.views import app

manager = Manager(app)
manager.add_command('assets', ManageAssets(assets))
logger = logging.getLogger(__name__)


@manager.command
def createdb():
    """ Make the database. """
    logger.info('Create DB')
    logger.info('Create Extensions')
    db.engine.execute("CREATE EXTENSION IF NOT EXISTS hstore;")
    db.engine.execute("CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;")
    db.create_all()


@manager.command
def flush(dataset):
    logger.info('Flushing')
    ds = Dataset.by_name(dataset)
    for alias in Alias.all_unmatched(ds):
        db.session.delete(alias)
    db.session.commit()


@manager.option('-h', '--host', dest='host', default='127.0.0.1')
@manager.option('-p', '--port', dest='port', type=int, default=8000)
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
