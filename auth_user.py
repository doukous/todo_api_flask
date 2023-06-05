from flask import Blueprint, jsonify


auth_bp = Blueprint('authentication', __name__, url_prefix='/auth')


@auth_bp.post('/login')
def log_a_user():
    return jsonify({'message': 'log a user'})


@auth_bp.post('/signup')
def sign_up():
    return jsonify({'message': 'sign-up a user'})
