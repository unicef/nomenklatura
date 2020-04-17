from flask.ext.assets import ManageAssets
from flask.ext.script import Manager

from nomenklatura.assets import assets
from nomenklatura.core import db
from nomenklatura.views import app

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


if __name__ == '__main__':
    manager.run()
