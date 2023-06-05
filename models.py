from flask_sqlalchemy import SQLAlchemy
from config import metadata


db = SQLAlchemy(metadata=metadata)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Task name : {self.name}'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    tasks = db.relationship('Task', backref='user')


    def __repr__(self):
        return f'Username : {self.username}'
