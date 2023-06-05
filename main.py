from flask import request, jsonify
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



@app.get('/user/<string:username>')
@jwt_required()
def get_all_user_tasks(username):
    task_schema = TaskSchema(many=True)

    user_jwt_id = get_jwt_identity()
    user = db.one_or_404(
        db.select(User).filter_by(username=username, id=user_jwt_id)
    )

    tasks_query_result = db.session.execute(
        db.select(Task).filter_by(user_id=user.id)
    ).scalars()
        
    tasks = task_schema.dump(tasks_query_result)

    return jsonify({'message': 'it works'})

@app.get('/users')
def get_all_users():
    schema = UserSchema(many=True)
   
    users_query_result = db.session.execute(db.select(User)).scalars()
    users = schema.dump(users_query_result)

    return users


@app.put('/user/<string:username>/<string:task_name>')
@jwt_required()
def edit_status_completion(username, task_name):
    task = Task(name=task_name)
    user = db.one_or_404(
        db.select(User).filter_by(username=username)
    )

    task = db.one_or_404(
        db.select(Task).filter_by(name=task_name, user_id=user.id))

    task.completed = not task.completed
    db.session.commit()

    message = f'Task {task.name} successfully edited'

    return jsonify(message)


@app.route('/user/<string:username>/<string:task_name>', 
           methods=['POST', 'DELETE'])
@jwt_required()
def edit_task_list(username, task_name):
    user = db.one_or_404(
        db.select(User).filter_by(username=username)
    )

    task = Task(name=task_name)

    if request.method == 'POST':
        task = Task(name=task_name)
        
        db.session.add(task)
        db.session.commit()

        message = 'Task successfully created'
        
        return jsonify(message)
    
    elif request.method == 'DELETE':
        user = db.one_or_404(
        db.select(User).filter_by(username=username)
        )

        task = db.one_or_404(
            db.select(Task).filter_by(name=task_name, user_id=user.id))

        db.session.delete(task)
        db.session.commit()

        message = 'Task successfully deleted'

        return jsonify(message)


if __name__ == '__main__':
    app.run()
