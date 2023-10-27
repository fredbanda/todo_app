from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:fred80@localhost:5432/todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)

@app.route("/")
def index():
    todo_list = Todo.query.all()
    total_todo = Todo.query.count()
    completed_todo = Todo.query.filter_by(complete=True).count()
    uncompleted_todo = total_todo - completed_todo
    return render_template('dashboard/index.html', **locals())


@app.route("/add", methods=['POST'])
def add():
    title = request.form.get('title')
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:id>")
def update(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))



@app.route("/addtodo")
def addtodo():
    return render_template('dashboard/addtodo.html', title='addtodo')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)