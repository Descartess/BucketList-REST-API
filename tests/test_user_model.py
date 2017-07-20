""" unit tests for the user model """
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import Users
from .test_config import ConfigTestCase


class UsersTestCase(ConfigTestCase):
    """ unit tests for the user model """
    def test_add_user(self):
        """ Ensure that user is added """
        user = Users(username="Paul")
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.id)
        self.assertEqual(user.username, "Paul")

    def test_duplicate_users(self):
        """ Ensure that duplicate users are not  added """
        user = Users(username="Paul")
        db.session.add(user)
        db.session.commit()
        duplicate_user = Users(username="Paul")
        db.session.add(duplicate_user)
        with self.assertRaises(IntegrityError):
            db.session.commit()


