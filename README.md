# M13_Backend12

 REST API  app with Authorization and Authentication


Запустіть контейнер з базою даних PostgreSQL командою:

```
docker run --name db-postgre -p 5432:5432 -e POSTGRES_PASSWORD=567234 -e POSTGRES_DB=contacts -d postgres
```

Для взаємодії з побудованим REST API, будемо використовувати Swagger документацію http://127.0.0.1:8000/docs


Для роботи проекта необхідний файл `.env` зі змінними оточення.
Створіть його з таким вмістом і підставте свої значення.

```dotenv
# Database PostgreSQL
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_PORT=

SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${POSTGRES_PORT}/${POSTGRES_DB}

# JWT authentication
SECRET_KEY=
ALGORITHM=

# Email service
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIL_PORT=
MAIL_SERVER=

# Redis
REDIS_HOST=
REDIS=

# Cloud Storage
CLOUDINARY_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

Запуск баз даних

```bash
docker-compose up -d
```

Запуск застосунку

```
uvicorn main:app --reload
```
