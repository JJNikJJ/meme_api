import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
import models

# Создание тестовой базы данных с использованием Postgres
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db:5432/memes"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Инициализация базы данных для тестов
Base.metadata.create_all(bind=engine)


# Переопределение зависимости get_db для использования тестовой базы данных
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# Функция для создания тестового мема
def create_test_meme():
    return client.post("/memes", json={"title": "Test Meme", "description": "Test Description",
                                       "image_url": "https://avatars.githubusercontent.com/u/99767736?v=4"})


# Тест создания мема
def test_create_meme():
    response = create_test_meme()
    assert response.status_code == 200
    assert response.json()["title"] == "Test Meme"


# Тест получения списка мемов
def test_read_memes():
    response = client.get("/memes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Тест получения конкретного мема по ID
def test_read_meme():
    create_response = create_test_meme()
    meme_id = create_response.json()["id"]
    response = client.get(f"/memes/{meme_id}")
    assert response.status_code == 200
    assert response.json()["id"] == meme_id


# Тест обновления мема
def test_update_meme():
    create_response = create_test_meme()
    meme_id = create_response.json()["id"]
    update_response = client.put(f"/memes/{meme_id}",
                                 json={"title": "Updated Meme", "description": "Updated Description",
                                       "image_url": "https://avatars.githubusercontent.com/u/99767736?v=4"})
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Meme"


# Тест удаления мема
def test_delete_meme():
    create_response = create_test_meme()
    meme_id = create_response.json()["id"]
    delete_response = client.delete(f"/memes/{meme_id}")
    assert delete_response.status_code == 200
    get_response = client.get(f"/memes/{meme_id}")
    assert get_response.status_code == 404
