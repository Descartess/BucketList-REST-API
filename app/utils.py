""" utility functions """
from functools import wraps
from flask import jsonify, request
from app import db
from app.models import Users

def add_user(username, password):
    """ Utility function that adds users to database """
    user = Users(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return user

def validate_auth_json(function):
    """ decorator function to validate authentication json """
    @wraps(function)
    def decorated(*args, **kwargs):
        """ Flask validation of authentication json """
        if request.method == "POST":
            post_data = request.get_json()
            if not post_data.get('username') or not post_data.get('password'):
                response_object = {
                    'status': 'Fail',
                    'message': 'Invalid payload',
                    'token': None
                }
                return jsonify(response_object),400
        return function(*args, **kwargs)
    return decorated

def login_required(function):
    """ utility  decorator function to check is user is authenticated """
    def decorated(*args, **kwargs):
        """ decorator function logic """
        return function(*args, **kwargs)
    return decorated



