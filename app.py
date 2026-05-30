from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields

app = Flask(__name__)

# =====================
# CONFIG
# =====================
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =====================
# MODEL
# =====================
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)

# IMPORTANT: create DB FIRST
with app.app_context():
    db.create_all()

# =====================
# WEB ROUTES (KEEP SIMPLE FIRST)
# =====================
@app.route("/")
def home():
    todos = Todo.query.all()
    return render_template("base.html", todo_list=todos)

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
# SWAGGER (ADD LAST — IMPORTANT FIX)
# =====================
api = Api(
    app,
    version="1.0",
    title="Flask Todo API",
    description="Todo API with Swagger UI",
    doc="/swagger"
)

ns = api.namespace("tasks", description="Todo operations")

todo_model = api.model("Todo", {
    "id": fields.Integer(readonly=True),
    "title": fields.String(required=True),
    "complete": fields.Boolean
})

@ns.route("/")
class TaskList(Resource):

    @ns.marshal_list_with(todo_model)
    def get(self):
        return Todo.query.all()

    @ns.expect(todo_model)
    def post(self):
        data = api.payload

        task = Todo(
            title=data["title"],
            complete=False
        )

        db.session.add(task)
        db.session.commit()

        return {"message": "created"}, 201


@ns.route("/<int:task_id>")
class Task(Resource):

    def get(self, task_id):
        task = Todo.query.get(task_id)
        if not task:
            return {"error": "not found"}, 404

        return {
            "id": task.id,
            "title": task.title,
            "complete": task.complete
        }

    def delete(self, task_id):
        task = Todo.query.get(task_id)
        if not task:
            return {"error": "not found"}, 404

        db.session.delete(task)
        db.session.commit()

        return {"message": "deleted"}

# =====================
# RUN APP
# =====================
if __name__ == "__main__":
    app.run(debug=True)
