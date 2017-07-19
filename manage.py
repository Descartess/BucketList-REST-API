""" manage.py """
from flask_script import Manager

from app import create_app, db

APP = create_app('default')

manager = Manager(APP)

if __name__ == "__main__":
    manager.run()
