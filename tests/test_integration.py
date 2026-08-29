import uuid

import psycopg
from fastapi.testclient import TestClient

from src.database import DATABASE_URL
from src.main import app


client = TestClient(app)


def test_create_user_and_check_database():
    email = f"integration_{uuid.uuid4().hex}@example.com"

    response = client.post(
        "/users",
        json={
            "email": email,
            "name": "Integration Test",
        },
    )

    assert response.status_code == 201

    connection = psycopg.connect(DATABASE_URL)

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT email, name, balance
            FROM users
            WHERE email = %s
            """,
            (email,),
        )

        user = cursor.fetchone()

    connection.close()

    assert user is not None
    assert user[0] == email
    assert user[1] == "Integration Test"
    assert float(user[2]) == 0.0