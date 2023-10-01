# Extract Engine Frontend

Extract Engine Frontend is the frontend for the Extract Engine service

## Architecture

- Extract Engine Frontend: Flask based service.
- Extract Engine Users API: Flask application managing users and login
- Extract Engine Open ai API: Flask application managing open ai calls
- SQS service: SQS queing system to handle webscraping requests

## Requirements
- Docker

## Installation

1. Clone the repositories into a new folder

```
git clone git@github.com:rachhtordoff/Extract-Engine-frontend.git
git clone git@github.com:rachhtordoff/Extract-Engine-users-api.git
git clone git@github.com:rachhtordoff/Extract-Engine-OpenAi-api.git
```
2. Create a docker-compose yaml file and place it in the route directory
```
x-user-gunicorn: &user-gunicorn
  gunicorn --bind 0.0.0.0:8000 --access-logfile - src:app --reload
x-openapi-gunicorn: &openapi-gunicorn
  gunicorn --bind 0.0.0.0:8010 --access-logfile - src:app --reload
x-frontend-gunicorn: &frontend-gunicorn
  gunicorn --bind 0.0.0.0:9010 --access-logfile - src:app --reload
x-openapi-gunicorn: &emailapi-gunicorn
  gunicorn --bind 0.0.0.0:8020 --access-logfile - src:app --reload

version: '3.8'
services:
  frontend:
    build: ./Extract-Engine-frontend
    volumes:
      - ./Extract-Engine-frontend:/opt
    ports:
      - "9010:9010"
    environment:
      - APP_NAME=company-insurance-frontend
      - FLASK_LOG_LEVEL=DEBUG
      - PYTHONPATH=/opt
      - FLASK_APP=manage.py
      - SECRET_KEY=you-will-never-guess
      - DEBUG=True
      - DEVELOPMENT=True
      - LOG_LEVEL=DEBUG
      - FOO=bar
      - user_api_url=http://user_api:8000/
      - openapi_api_url=http://openapi_api:8010/
      - JWT_SECRET_KEY=super-secret-key
      - email_api_url=http://email_api:8020/
      - LOGIN_URL=http://localhost:9010

    labels:
      - "traefik.http.routers.frontend.rule=Host(`frontend.docker.localhost`)"
    command: *frontend-gunicorn
    depends_on:
      - user_api
      - openapi_api  

  user_api:
    build: ./Extract-Engine-users-api
    volumes:
      - ./Extract-Engine-users-api:/opt
    ports:
     - "8000:8000"
    environment:
     - APP_NAME=company-insurance-frontend
     - FLASK_LOG_LEVEL=DEBUG
     - PYTHONPATH=/opt
     - FLASK_APP=manage.py
     - SECRET_KEY=you-will-never-guess
     - POSTGRES_USER=db_user
     - POSTGRES_PASSWORD=password
     - POSTGRES_DB=user_db
     - POSTGRES_HOST=postgres
     - POSTGRES_PORT=5432
     - DEBUG=True
     - DEVELOPMENT=True
     - DATABASE_URL=postgresql://db_user:password@db:5432/user_db
     - LOG_LEVEL=DEBUG
     - FOO=bar
     - JWT_SECRET_KEY=super-secret-key

    labels:
      - "traefik.http.routers.app.rule=Host(`app.docker.localhost`)"
    command: *user-gunicorn

  openapi_api:
    build: ./Extract-Engine-OpenAi-api
    volumes:
      - ./Extract-Engine-OpenAi-api:/opt
    ports:
      - "8010:8010"
    environment:
      - APP_NAME=company-insurance-frontend
      - FLASK_LOG_LEVEL=DEBUG
      - PYTHONPATH=/opt
      - FLASK_APP=manage.py
      - OPENAPI_KEY=your-key-here
      - SECRET_KEY=xyz
      - DEBUG=True
      - DEVELOPMENT=True
      - LOG_LEVEL=DEBUG
      - FOO=bar
      - APIKEY=xxx
      - JWT_SECRET_KEY=super-secret-key
      - POSTGRES_USER=db_user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=machinelearning_db
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - DATABASE_URL=postgresql://db_user:password@db:5432/machinelearning_db
    labels:
      - "traefik.http.routers.app.rule=Host(`app.docker.localhost`)"
    command: *openapi-gunicorn

  email_api:
    build: ./email-api
    volumes:
      - ./email-api:/opt
    ports:
      - "8020:8020"
    environment:
      - FLASK_APP=manage.py
      - APP_NAME=email-api
      - FLASK_LOG_LEVEL=DEBUG
      - PYTHONPATH=/opt
      - ADMINS=test@gmail.com
      - EMAIL_TIME_CHECK=30
      - SECRET_KEY=you-will-never-guess
      - RECIPIENT=email-provider-here
      - APM_ENABLED=False
      - MAIL_SERVER=smtp.gmail.com
      - MAIL_PORT=587
      - MAIL_USERNAME=remail-provider-here
      - MAIL_PASSWORD=mail-password-here
      - DEBUG=True
      - DEVELOPMENT=True
      - JWT_SECRET_KEY=super-secret-key

    command: *emailapi-gunicorn
        
  postgres:
    image: postgres:9.6
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=db_user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=postgres
    volumes:
      - ./tables:/docker-entrypoint-initdb.d/
      - ./data:/var/lib/postgresql/data
    
  reverse-proxy:
    image: traefik:v2.9
    command: --api.insecure=true --providers.docker
    ports:
      - "80:80"
      - "8080:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock

  sqs:
    image: softwaremill/elasticmq
    ports:
      - 9324:9324
    volumes:
      - ./config/sqs/custom.conf:/opt/elasticmq.conf

volumes:
  db-data:
```

3. Build the Docker compose:
```
docker-compose up --build -d
```

## Run Unit tests
```
docker-compose run frontend python -m unittest
```


## Run linting
```
docker-compose run frontend flake8 ./
```
