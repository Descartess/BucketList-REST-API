""" unit tests for config.py """

import unittest

from flask import current_app
from app import create_app, db

class ConfigTestCase(unittest.TestCase):
    """ unit tests for basic config and setup"""
    def setUp(self):
        """initial setup before a test is run """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """executes  after a test is run """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        """ test if app exists"""
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """ test if app config is testing """
        self.assertFalse(self.app.config['DEBUG'])
        