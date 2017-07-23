""" Authentication functionality """
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import Users

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/register', methods=['POST'])
def register():
    """ Register a new user """
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'Fail',
            'message': 'Invalid payload'
        }
        return jsonify(response_object), 400
    username = post_data.get('username')
    password = post_data.get('password')
    try:
        user = Users.query.filter_by(username=username).first()
        if not user:
            db.session.add(Users(username=username, password=password))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': username
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'Fail',
                'message': "Sorry username already is taken"
            }
            return jsonify(response_object), 400
    except IntegrityError:
        db.session().rollback()
        response_object = {
            'status': 'Fail',
            'message': "Invalid payload"
        }
        return jsonify(response_object), 400