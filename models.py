from flask_sqlalchemy import SQLAlchemy
from config import metadata


db = SQLAlchemy(metadata=metadata)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(30), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_affiliated = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False
    )

    def __repr__(self):
        return f'<Task : {self.text}>'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(), nullable=False)
    tasks = db.relationship('Task', backref='user', passive_deletes=True)
    
    
    def __repr__(self):
        return f'<Username : {self.username}>'
