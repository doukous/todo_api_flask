from marshmallow import fields, Schema, post_load
from models import User, Task


class TaskSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    completed = fields.Bool()
    user_id = fields.Int(required=True)


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str(required=True)
    password = fields.String(required=True)
    email = fields.Email(required=True)
    tasks = fields.List(fields.Nested(Task))

    