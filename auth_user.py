from flask import Blueprint, jsonify, request
from schemas import UserSchema
from models import db, User
from flask_jwt_extended import create_access_token


auth_bp = Blueprint('authentication', __name__, url_prefix='/auth')


@auth_bp.post('/login')
def log_in(): 
    data = request.get_json()
    user_schema = UserSchema(only=("email", "password"))
    user = user_schema.load(data)

    user_query_result = db.one_or_404(
        db.select(User).filter_by(
        email=user["email"], password=user["password"])
    )

    if user_query_result:
        user_token = create_access_token(user_query_result.id)
        message = 'log a user'

        return jsonify(message, user_token)
    
    return jsonify(message="user not found"), 404


@auth_bp.post('/signup')
def sign_up():
    data = request.get_json()
    
    user_schema = UserSchema().load(data)
    user = User(**user_schema)

    db.session.add(user)
    db.session.commit()

    message = 'sign-up a user'

    return jsonify(message)
