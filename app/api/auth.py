""" Authentication functionality """
from flask import Blueprint, jsonify, request, current_app
from sqlalchemy.exc import IntegrityError
from app import db, bcrypt
from app.utils import add_user, validate_auth_json,login_required
from app.models import Users

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/register', methods=['POST'])
@validate_auth_json
def register():
    """ Register a new user """
    post_data = request.get_json()
    username = post_data.get('username')
    password = post_data.get('password')
    try:
        user = Users.query.filter_by(username=username).first()
        if not user:
            user = add_user(username, password)
            response_object = {
                'status': 'success',
                'message': username,
                'token': user.encode_auth_token(user.id).decode()
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'Fail',
                'message': "Sorry username already is taken",
                'token': None
            }
            return jsonify(response_object), 400
    except IntegrityError:
        db.session().rollback()


@auth_blueprint.route('/login', methods=["POST"])
@validate_auth_json
def login():
    """ Login in old users """
    post_data = request.get_json()
    username = post_data.get('username')
    password = post_data.get('password')
    try:
        user = Users.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_object = {
                    'status': 'Success',
                    'token': auth_token.decode()
                }
                return jsonify(response_object), 200
        response_object = {
            'status': 'Fail',
            'message': 'Invalid credentials',
            'token': None
        }
        return jsonify(response_object), 400
    except Exception as e:
        response_object = {
            'status': 'Fail',
            'message': 'Invalid credentials',
            'token': None
        }
        return jsonify(response_object), 400


@auth_blueprint.route('/reset-password', methods=["POST"])
@login_required
def reset_password(user):
    """ Enable users to reset passwords """
    post_data = request.get_json()
    old_password = post_data.get('old_password')
    new_password = post_data.get('new_password')
    # check if old password is correct
    if bcrypt.check_password_hash(user.password, old_password):
        user.password = bcrypt.generate_password_hash(
            new_password, current_app.config.get('BCRYPT_LOG_ROUNDS'))
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        if auth_token:
            response_object = {
                "status": "Success",
                "mesage": "Password changed",
                "token": auth_token.decode()
            }
            return jsonify(response_object), 201
    response_object = {
        "status": "Fail",
        "mesage": "Invalid credentials",
        "token": None
    }
    return jsonify(response_object), 400

@auth_blueprint.route('/logout', methods=["GET"])
@login_required
def logout(user):
    """ Log out user """
    response_object = {
        "status" : "Success",
        "message": " Log Out successful"
    }
    return jsonify(response_object), 200
