import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import get_db, Base
from app.core.config import settings

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestQuranAPI:
    def test_get_surahs(self):
        response = client.get("/api/v1/quran/surahs")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_surah_by_number(self):
        response = client.get("/api/v1/quran/surahs/1")
        assert response.status_code == 200
        data = response.json()
        assert data["number"] == 1
        assert data["name_english"] == "Al-Fatihah"

    def test_get_surah_not_found(self):
        response = client.get("/api/v1/quran/surahs/999")
        assert response.status_code == 404

    def test_get_surah_with_ayahs(self):
        response = client.get("/api/v1/quran/surahs/1/ayahs")
        assert response.status_code == 200
        data = response.json()
        assert "ayahs" in data
        assert len(data["ayahs"]) == 7  # Al-Fatihah has 7 ayahs

    def test_get_specific_ayah(self):
        response = client.get("/api/v1/quran/surahs/1/ayahs/1")
        assert response.status_code == 200
        data = response.json()
        assert data["ayah_number"] == 1
        assert "arabic_text" in data
        assert "english_translation" in data

    def test_get_juzs(self):
        response = client.get("/api/v1/quran/juzs")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_search_quran(self):
        response = client.get("/api/v1/quran/search?q=mercy&language=english")
        assert response.status_code == 200
        data = response.json()
        assert "ayahs" in data
        assert "total" in data
        assert "page" in data
        assert "per_page" in data

    def test_random_ayah(self):
        response = client.get("/api/v1/quran/random-ayah")
        assert response.status_code == 200
        data = response.json()
        assert "arabic_text" in data
        assert "english_translation" in data


class TestHealthCheck:
    def test_health_endpoint(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
