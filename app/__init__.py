""" __init__.py """
from flask import Flask, jsonify

APP = Flask(__name__)

@APP.route('/', methods=['GET'])
def index():
    """ initial dummy route """
    return jsonify({
        'status': 'success',
        'message': 'this was a success'
    })
