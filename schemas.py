from marshmallow import fields, Schema


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str(required=True)
    password = fields.String(required=True)
    email = fields.Email(required=True)


class TaskSchema(Schema):
    id = fields.Int()
    text = fields.Str(required=True)
    completed = fields.Bool()
    user_affiliated = fields.Int()
