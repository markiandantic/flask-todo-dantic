import json
from app import app, db, Todo


def setup_module(module):
    app.config["TESTING"] = True

    with app.app_context():
        db.drop_all()
        db.create_all()


def test_create_task():
    client = app.test_client()

    response = client.post(
        "/api/tasks",
        json={"title": "Study Flask"}
    )

    assert response.status_code == 201


def test_get_all_tasks():
    client = app.test_client()

    response = client.get("/api/tasks")

    assert response.status_code == 200


def test_get_single_task():
    client = app.test_client()

    response = client.get("/api/tasks/1")

    assert response.status_code == 200


def test_update_task():
    client = app.test_client()

    response = client.put(
        "/api/tasks/1",
        json={
            "title": "Updated Task",
            "complete": True
        }
    )

    assert response.status_code == 200


def test_delete_task():
    client = app.test_client()

    response = client.delete("/api/tasks/1")

    assert response.status_code == 200


def test_get_invalid_task():
    client = app.test_client()

    response = client.get("/api/tasks/999")

    assert response.status_code == 404


def test_create_task_without_title():
    client = app.test_client()

    response = client.post(
        "/api/tasks",
        json={}
    )

    assert response.status_code == 400