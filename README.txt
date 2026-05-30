FLASK TODO APPLICATION WITH REST API AND SWAGGER

DESCRIPTION:
This project is a Todo application built using Flask.
It has both a web interface and a REST API with Swagger documentation.

FEATURES:
- Add Todo
- Update Todo (mark complete/incomplete)
- Delete Todo
- View all todos (Web UI)
- REST API support
- Swagger UI for API testing

ENDPOINTS:
GET    /api/tasks          - Get all tasks
POST   /api/tasks          - Create task
GET    /api/tasks/<id>     - Get single task
PUT    /api/tasks/<id>     - Update task
DELETE /api/tasks/<id>     - Delete task

HOW TO RUN:
1. Install dependencies:
   pip install -r requirements.txt

2. Run the app:
   python app.py

3. Open in browser:
   Web App: http://127.0.0.1:5000/
   Swagger: http://127.0.0.1:5000/swagger

TECH STACK:
- Python
- Flask
- Flask-SQLAlchemy
- Flask-RESTX
- SQLite