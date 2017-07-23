""" unit tests for the user model """
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import Users
from .test_base import BaseTestCase
from .test_utils import add_user


class UsersTestCase(BaseTestCase):
    """ unit tests for the user model """

    def test_add_user(self):
        """ Ensure that user is added """
        user = Users(username="Paul", password="password")
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.id)
        self.assertEqual(user.username, "Paul")

    def test_duplicate_users(self):
        """ Ensure that duplicate users are not  added """
        user = Users(username="Paul", password="pass")
        db.session.add(user)
        db.session.commit()
        duplicate_user = Users(username="Paul", password="test")
        db.session.add(duplicate_user)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_missing_password(self):
        """ Ensure that an error is returned on missing password """
        with self.assertRaises(TypeError):
            user = Users(username="Paul")

    def test_missing_username(self):
        """ Ensure that an error is returned on missing username """
        with self.assertRaises(TypeError):
            user = Users(password="Paul")

    def test_encode_auth_token(self):
        """ Ensure that authentication token is returned after user registration """
        user = add_user(username="Paul", password="password")
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        """ Ensure that authentication token is correctly decoded """
        user = add_user(username="Paul", password="password")
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(Users.decode_auth_token(auth_token), user.id)
