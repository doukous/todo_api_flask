from flask import request, jsonify
from models import db, Task, User
from flask_migrate import Migrate
from config import app
from schemas import TaskSchema, UserSchema
from auth_user import auth_bp


app.register_blueprint(auth_bp)
db.init_app(app)
migrate = Migrate(app, db)


@app.get('/user/<string:username>')
def get_all_tasks(username):
    schema = TaskSchema(many=True)
    username = User(username=username)

    tasks_query_result = db.session.execute(db.select(Task).filter_by(user_id=username.id)).scalars()
    tasks = schema.dump(tasks_query_result)

    return tasks

@app.get('/users')
def get_all_users():
    schema = UserSchema(many=True)
   
    users_query_result = db.session.execute(db.select(User)).scalars()
    users = schema.dump(users_query_result)

    return users


@app.put('/user/<string:username>/<string:task_name>')
def edit_status_completion(username, task_name):
    username = User(username=username)
    task = Task(name=task_name)

    task = db.one_or_404(db.select(Task).filter_by(name=task_name, user_id=username.id))

    task.completed = not task.completed
    db.session.commit()

    return jsonify({'message': f'Task {task.username} successfully edited'})


@app.route('/user/<string:username>/<string:task_name>', methods=['POST', 'DELETE'])
def edit_task_list(username, task_name):
    username = User(username=username)
    task = Task(name=task_name)

    if request.method == 'POST':
        task = Task(name=task_name)
        
        db.session.add(task)
        db.session.commit()

        return jsonify({'message': 'Task successfully created'})
    
    elif request.method == 'DELETE':
        task = db.one_or_404(db.select(Task).filter_by(name=task_name, user_id=username.id))

        db.session.delete(task)
        db.session.commit()

        return jsonify({'message': 'Task successfully deleted'})


if __name__ == '__main__':
    app.run()
