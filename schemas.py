from marshmallow import fields, Schema
from models import Task


class TaskSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    completed = fields.Bool()
    user_id = fields.Int(required=True)


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    password = fields.String()
    email = fields.Email()
    tasks = fields.List(fields.Nested(Task))
    