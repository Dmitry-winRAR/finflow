import uuid

import psycopg


def test_deposit_updates_user_balance(client, db_connection):
    email = f"transaction_{uuid.uuid4().hex}@example.com"

    create_response = client.post(
        "/users",
        json={
            "email": email,
            "name": "Transaction Test",
        },
    )

    assert create_response.status_code == 201

    with db_connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, balance FROM users WHERE email = %s",
            (email,),
        )
        user = cursor.fetchone()

    assert user is not None

    user_id = user[0]
    initial_balance = float(user[1])

    transaction_response = client.post(
        "/transactions",
        json={
            "user_id": user_id,
            "amount": 100.00,
            "type": "deposit",
        },
    )

    assert transaction_response.status_code == 201

    with db_connection.cursor() as cursor:
        cursor.execute(
            "SELECT balance FROM users WHERE id = %s",
            (user_id,),
        )
        balance = cursor.fetchone()

    assert balance is not None
    assert float(balance[0]) == initial_balance + 100.00