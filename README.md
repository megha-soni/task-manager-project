# Task Manager API

A simple and scalable Task Manager API built using Django REST Framework with JWT Authentication.

## 🚀 Features

- User authentication using JWT
- Create a task
- Get all tasks
- Get single task details
- Mark task as completed
- Delete task
- Filter tasks (Completed / Pending)
- Search tasks by title

## 🛠 Tech Stack

- Python
- Django
- Django REST Framework
- JWT Authentication

## 📦 Setup Instructions

```bash
git clone https://github.com/megha-soni/task-manager-project.git
cd task-manager-project

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser

python manage.py runserver
