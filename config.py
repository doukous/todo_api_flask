from datetime import timedelta
from secrets import token_hex
from flask import Flask
from sqlalchemy import MetaData


jwt_secret = 'test'

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = jwt_secret
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)


app = Flask(__name__)
app.config.from_object('config.Config')

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)