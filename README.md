## FastAPI Application

This FastAPI application serves as a comprehensive platform to manage user accounts and jokes. It provides robust APIs for CRUD (Create, Read, Update, Delete) operations, tailored for authenticated users. The key features include:

User Management: Allows users to create, edit, and delete their accounts seamlessly.

Joke Management: Enables users to add, retrieve, update, and delete jokes with ease.

Automated Joke Fetching: Integrates with an external joke API to fetch and store a new joke every minute automatically. This ensures the joke database is continuously enriched with fresh content.

This application is designed to be simple to set up and highly interactive through FastAPI’s built-in documentation tools.

Note: 1. Only the creator of joke can delete the user
      2. If user edits his email, he needs to login and get token again using the updated email.
      3. Passing token is needed for every API.

## Setup
### Environment setup
```
> python3 -m venv venv
(python 3.13 is used)

> source venv/bin/activate
> python3 -m pip install -r requirements.txt
> export PYTHONPATH=$PWD
```

## Redis, Celery, and Celery Beat Setup

Start Redis
Ensure Redis is installed and running. You can start it with:
> redis-server

Run Celery Worker
Start the Celery worker to handle background tasks:
> cd app
> celery -A celery_worker.celery_app worker --loglevel=info

Run Celery Beat Scheduler
Start the Celery beat scheduler to manage periodic tasks:
> cd app
> celery -A celery_worker.celery_app beat --loglevel=info



### Settings
Add file named `.env` and add the appropriate values.

## Run the Project
```
> cd app
> export PYTHONPATH=$PYTHONPATH:"Project folder path"   ## make sure to replace your folder path here.
> python3 main.py
```

## API Documentation

FastAPI provides interactive API documentation that can be accessed in your browser once the application is running, Use these tools to understand available endpoints, required parameters, and responses.

To test or verify:
    Example URL: http://127.0.0.1:8000/docs
    Description: Swagger UI offers a user-friendly interface for exploring and testing APIs.

Documentation:
    example URL: http://127.0.0.1:8000/redoc
    Description: ReDoc provides a clean and comprehensive view of the API schema and documentation.

