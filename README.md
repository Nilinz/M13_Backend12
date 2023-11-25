# M13_Backend12

 REST API  app with Authorization and Authentication


Запустіть контейнер з базою даних PostgreSQL командою:

```
docker run --name db-postgre -p 5432:5432 -e POSTGRES_PASSWORD=567234 -e POSTGRES_DB=contacts -d postgres
```

Запускаємо сервер:

```
uvicorn app.main:app --reload
```



Для взаємодії з побудованим REST API, будемо використовувати Swagger документацію http://127.0.0.1:8000/docs


