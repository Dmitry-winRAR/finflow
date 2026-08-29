import psycopg
import pytest
from fastapi.testclient import TestClient

from src.database import DATABASE_URL
from src.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db_connection():
    connection = psycopg.connect(DATABASE_URL)

    yield connection

    connection.close()