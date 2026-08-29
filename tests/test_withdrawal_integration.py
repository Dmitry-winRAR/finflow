import uuid


def test_withdrawal_updates_user_balance(client, db_connection):
    email = f"withdrawal_{uuid.uuid4().hex}@example.com"

    create_response = client.post(
        "/users",
        json={
            "email": email,
            "name": "Withdrawal Test",
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

    deposit_response = client.post(
        "/transactions",
        json={
            "user_id": user_id,
            "amount": 200.00,
            "type": "deposit",
        },
    )

    assert deposit_response.status_code == 201

    withdrawal_response = client.post(
        "/transactions",
        json={
            "user_id": user_id,
            "amount": 75.00,
            "type": "withdrawal",
        },
    )

    assert withdrawal_response.status_code == 201

    with db_connection.cursor() as cursor:
        cursor.execute(
            "SELECT balance FROM users WHERE id = %s",
            (user_id,),
        )
        balance = cursor.fetchone()

    assert balance is not None
    assert float(balance[0]) == 125.00