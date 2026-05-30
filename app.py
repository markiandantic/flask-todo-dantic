from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields

app = Flask(__name__)

# =====================
# DATABASE CONFIG
# =====================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =====================
# SWAGGER SETUP (FIXED)
# =====================
api = Api(
    app,
    version="1.0",
    title="Flask Todo API",
    description="Todo API with Swagger UI",
    doc="/swagger"   # 👉 http://127.0.0.1:5000/swagger
)

# IMPORTANT: FIXED namespace (no duplicate path)
ns = api.namespace("tasks", description="Todo operations")

# =====================
# MODEL
# =====================
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

# =====================
# SWAGGER MODEL
# =====================
todo_model = api.model("Todo", {
    "id": fields.Integer(readonly=True),
    "title": fields.String(required=True),
    "complete": fields.Boolean
})

# =====================
# WEB ROUTES
# =====================
@app.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")

    if title:
        db.session.add(Todo(title=title, complete=False))
        db.session.commit()

    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.get(todo_id)

    if todo:
        todo.complete = not todo.complete
        db.session.commit()

    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.get(todo_id)

    if todo:
        db.session.delete(todo)
        db.session.commit()

    return redirect(url_for("home"))

# =====================
# REST API (SWAGGER ENABLED)
# =====================

@ns.route("/")
class TaskList(Resource):

    @ns.marshal_list_with(todo_model)
    def get(self):
        return Todo.query.all()

    @ns.expect(todo_model)
    @ns.marshal_with(todo_model, code=201)
    def post(self):
        data = api.payload

        if not data or not data.get("title"):
            api.abort(400, "Title is required")

        task = Todo(title=data["title"], complete=False)

        db.session.add(task)
        db.session.commit()
        return task, 201


@ns.route("/<int:task_id>")
class Task(Resource):

    @ns.marshal_with(todo_model)
    def get(self, task_id):
        task = Todo.query.get(task_id)

        if not task:
            api.abort(404, "Task not found")

        return task

    @ns.expect(todo_model)
    @ns.marshal_with(todo_model)
    def put(self, task_id):
        task = Todo.query.get(task_id)

        if not task:
            api.abort(404, "Task not found")

        data = api.payload

        task.title = data.get("title", task.title)
        task.complete = data.get("complete", task.complete)

        db.session.commit()
        return task

    def delete(self, task_id):
        task = Todo.query.get(task_id)

        if not task:
            api.abort(404, "Task not found")

        db.session.delete(task)
        db.session.commit()

        return {"message": "Task deleted successfully"}, 200


# =====================
# RUN APP
# =====================
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )