from pprint import pprint
from flask import Blueprint, jsonify, request
from schemas import UserSchema


auth_bp = Blueprint('authentication', __name__, url_prefix='/auth')


@auth_bp.post('/login')
def log_a_user():    
    return jsonify({'message': 'log a user'})


@auth_bp.post('/signup')
def sign_up():
    data = request.get_json()
    user_schema = UserSchema()
    user_info = user_schema.load(data)

    pprint(user_info)

    return jsonify({'message': 'sign-up a user'})
