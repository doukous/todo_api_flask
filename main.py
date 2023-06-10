import json
from flask import jsonify, request
from flask.views import MethodView
from models import db, Task, User
from flask_migrate import Migrate
from config import app
from schemas import TaskSchema, UserSchema
from auth_user import auth_bp
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity


app.register_blueprint(auth_bp)
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)


@app.get('/users')
def get_all_users():
    schema = UserSchema(many=True)
   
    users_query_result = db.session.execute(
        db.select(User)
        ).scalars()
    users = schema.dump(users_query_result)

    return users


def get_user_task(username):
    token_info = get_jwt_identity()
    text = request.get_json()["text"]

    user = db.one_or_404(
            db.select(User).filter_by(username=username, id=token_info['id'])
        )

    task = db.one_or_404(
        db.select(Task).filter_by(text=text, user_affiliated=user.id)
    )

    return task


class TaskOperation(MethodView):
    @jwt_required()
    def get(self, username):
        token_info = get_jwt_identity()
        user = db.one_or_404(
            db.select(User).filter_by(username=username, id=token_info['id'])
        )

        task_schema = TaskSchema(many=True)
        tasks = task_schema.dumps(user.tasks)
        
        return tasks
        

    @jwt_required()
    def post(self, username):
        token_info = get_jwt_identity()
        text = request.get_json()['text']

        user = db.one_or_404(
            db.select(User).filter_by(username=username, id=token_info['id'])
        )

        task = db.session.execute(
        db.select(Task).filter_by(text=text, user_affiliated=user.id)
        ).scalar_one_or_none()

        if not task:
            task = Task(text=text, user=user)
            db.session.add(task)
            db.session.commit()

            created_task = TaskSchema().dumps(task)

            return created_task
        
        else:
            return jsonify({'message': 'Task already exists'}), 208


    @jwt_required()
    def put(self, username):
        task = get_user_task(username)
        task.completed = not task.completed
        db.session.commit()

        edited_task = TaskSchema().dumps(task)

        return edited_task


    @jwt_required()
    def delete(self, username):
        task = get_user_task(username)
        
        db.session.delete(task)
        db.session.commit()

        deleted_task = TaskSchema().dumps(task)

        return deleted_task


def add_fake_user():
    with open("./fake_data.json", "r", encoding='utf-8') as f:
        data_list = json.load(f)

        for data_dict in data_list:
            tasks = data_dict["tasks"]

            user_obj = User(
                username = data_dict["username"],
                email = data_dict["email"],
                password = data_dict["password"], 
                )
            
            with app.app_context():
                db.session.add(user_obj)
                db.session.commit()

            for task in tasks:
                task_obj = Task(text=task, user=user_obj)

                with app.app_context():
                    db.session.add(task_obj)
                    db.session.commit()


app.add_url_rule(
    "/user/<string:username>",
    view_func=TaskOperation.as_view('task_operations')
)


if __name__ == '__main__':
    app.run()
