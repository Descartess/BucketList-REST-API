""" manage.py """
from flask_script import Manager

from app import APP

APP.config.from_object('config.DevelopmentConfig')

manager = Manager(APP)

if __name__ == "__main__":
    manager.run()
