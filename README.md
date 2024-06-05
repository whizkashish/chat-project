
# Chat Project

This is a chat application built with Django, Celery, Redis, and PostgreSQL. It supports real-time notifications and messaging.

## Features

- User authentication and profile management
- Real-time chat functionality
- Notification system
- RESTful API for integration with other services

## Requirements

- Docker and Docker Compose
- Python 3.9
- Django 3.x
- Celery
- Redis
- PostgreSQL

## Installation

### Clone the Repository

```bash
git clone https://github.com/whizkashish/chat-project.git
cd chat-project
```

### Set Up Environment Variables

Create a `.env` file in the project root directory and set the following environment variables:

```
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=devdb
DB_USER=devuser
DB_PASS=changeme
DB_HOST=db
REDIS_HOST=redis
REDIS_PORT=6379
BASE_URL=http://yourdomain.com
```

### Build and Run Docker Containers

```bash
docker-compose up --build
```

This command will build the Docker images and start the containers for the app, PostgreSQL, and Redis.

### Run Migrations and Collect Static Files

Open a new terminal and run the following commands:

```bash
docker-compose exec app python manage.py migrate
docker-compose exec app python manage.py collectstatic --noinput
```

## Configuration

### Django Settings

In `settings.py`, make sure the following settings are configured correctly:

```python
STATIC_URL = '/static/'
MEDIA_URL = '/files/'

MEDIA_ROOT = '/vol/web/media'
STATIC_ROOT = '/vol/web/static'
```

### Celery Configuration

Celery is configured in `celery.py` and used in the Django project to handle asynchronous tasks.

```python
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
```

## Usage

### Access the Application

Once the containers are running, you can access the application at `http://localhost:8000`.

### Running Celery

Celery is already set up to run within the Docker containers. You can view Celery logs with:

```bash
docker-compose logs -f celery
```

### Admin Panel

To access the Django admin panel, create a superuser:

```bash
docker-compose exec app python manage.py createsuperuser
```

Access the admin panel at `http://localhost:8000/admin`.


This README should help users set up and understand your project quickly.