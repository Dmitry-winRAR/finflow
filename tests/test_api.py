from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "FinFlow API is running"
    }


def test_get_users():
    response = client.get("/users")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_existing_user():
    response = client.get("/users/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["email"] == "dmitry@test.com"
    assert data["name"] == "Dmitry"


def test_get_nonexistent_user():
    response = client.get("/users/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_create_user():
    email = "pytest_user_2@example.com"

    response = client.post(
        "/users",
        json={
            "email": email,
            "name": "Pytest User",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == email
    assert data["name"] == "Pytest User"
    assert data["balance"] == 0.0


def test_create_deposit():
    response = client.post(
        "/transactions",
        json={
            "user_id": 1,
            "amount": 100,
            "type": "deposit",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["user_id"] == 1
    assert data["amount"] == 100.0
    assert data["type"] == "deposit"
    assert data["status"] == "pending"


def test_create_withdrawal():
    response = client.post(
        "/transactions",
        json={
            "user_id": 1,
            "amount": 30,
            "type": "withdrawal",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["user_id"] == 1
    assert data["amount"] == 30.0
    assert data["type"] == "withdrawal"


def test_transaction_unknown_user():
    response = client.post(
        "/transactions",
        json={
            "user_id": 999999,
            "amount": 100,
            "type": "deposit",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_transaction_negative_amount():
    response = client.post(
        "/transactions",
        json={
            "user_id": 1,
            "amount": -100,
            "type": "deposit",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "Amount must be greater than zero"


def test_transaction_invalid_type():
    response = client.post(
        "/transactions",
        json={
            "user_id": 1,
            "amount": 100,
            "type": "payment",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "Invalid transaction type"


def test_withdrawal_insufficient_balance():
    response = client.post(
        "/transactions",
        json={
            "user_id": 1,
            "amount": 1000000,
            "type": "withdrawal",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient balance"