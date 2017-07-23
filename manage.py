""" manage.py """
from flask_script import Manager

from app import create_app, db

APP = create_app('default')

manager = Manager(APP)

@manager.command
def recreate_db():
    """ Recreates a database """
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    manager.run()
