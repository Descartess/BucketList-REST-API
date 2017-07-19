""" unit tests for config.py """

from flask import current_app
from flask_testing import TestCase

from  app import APP

class TestDevelopmentConfig(TestCase):
    """ unit tests for Developement config """
    def create_app(self):
        """Flask testing intialization """
        APP.config.from_object('config.DevelopmentConfig')
        return APP

    def test_app_is_development(self):
        """ test development configuration """
        self.assertFalse(current_app is None)
        self.assertTrue(APP.config['DEBUG'] is True)
        self.assertTrue(APP.config['SQLALCHEMY_DATABASE_URI'] ==
                        'postgresql://postgres:qwerty@localhost:5432/bucketlist')




