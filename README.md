# Meme API

## Описание

Это веб-приложение на Python, использующее FastAPI, которое предоставляет API для работы с коллекцией мемов. Приложение состоит из двух сервисов: сервис с публичным API с бизнес-логикой и сервис для работы с медиа-файлами, используя S3-совместимое хранилище (например, MinIO).

## Функциональность

- **GET /memes**: Получить список всех мемов (с пагинацией).
- **GET /memes/{id}**: Получить конкретный мем по его ID.
- **POST /memes**: Добавить новый мем (с картинкой и текстом).
- **PUT /memes/{id}**: Обновить существующий мем.
- **DELETE /memes/{id}**: Удалить мем.

## Установка и запуск

1. Клонируйте репозиторий:

```sh
git clone https://github.com/yourusername/meme_api.git
cd meme_api
```

2. Запустите Docker Compose:

```sh
docker-compose up --build
 ```

3. Публичное API приложение будет доступно по адресу `http://localhost:8000`.

4. Документация публичного API будет доступна по адресу `http://localhost:8000/docs`.

5. Сервис для работы с медиа-файлами будет доступен по адресу `http://localhost:8001`.

6. Документация сервиса для работы с медиа-файлами будет доступен по адресу `http://localhost:8001/docs`.

## Запуск тестов

Для запуска тестов используйте следующую команду:

```sh
docker-compose up --build test
```

## Обработка ошибок и валидация входных данных

- Валидация входных данных осуществляется с помощью Pydantic моделей (`schemas.py`).
- Обработка ошибок реализована через использование исключений `HTTPException` в FastAPI.

## Использование Swagger/OpenAPI для документирования API

- FastAPI автоматически генерирует документацию API, доступную по адресу `/docs`.