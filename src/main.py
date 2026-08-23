
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.database import get_connection

app = FastAPI()


class UserCreate(BaseModel):
    email: str
    name: str


class TransactionCreate(BaseModel):
    user_id: int
    amount: float
    type: str


@app.get("/")
def root():
    return {"message": "FinFlow API is running"}


@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (email, name)
                VALUES (%s, %s)
                RETURNING id, email, name, balance, created_at
                """,
                (user.email, user.name),
            )

            new_user = cursor.fetchone()
            connection.commit()

            return {
                "id": new_user[0],
                "email": new_user[1],
                "name": new_user[2],
                "balance": float(new_user[3]),
                "created_at": new_user[4],
            }

    finally:
        connection.close()


@app.get("/users")
def get_users():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, email, name, balance, created_at
                FROM users
                ORDER BY id
                """
            )

            users = cursor.fetchall()

            return [
                {
                    "id": user[0],
                    "email": user[1],
                    "name": user[2],
                    "balance": float(user[3]),
                    "created_at": user[4],
                }
                for user in users
            ]

    finally:
        connection.close()


@app.get("/users/{user_id}")
def get_user(user_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, email, name, balance, created_at
                FROM users
                WHERE id = %s
                """,
                (user_id,),
            )

            user = cursor.fetchone()

            if user is None:
                raise HTTPException(
                    status_code=404,
                    detail="User not found",
                )

            return {
                "id": user[0],
                "email": user[1],
                "name": user[2],
                "balance": float(user[3]),
                "created_at": user[4],
            }

    finally:
        connection.close()


@app.post("/transactions", status_code=201)
def create_transaction(transaction: TransactionCreate):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                "SELECT balance FROM users WHERE id = %s",
                (transaction.user_id,),
            )

            user = cursor.fetchone()

            if user is None:
                raise HTTPException(
                    status_code=404,
                    detail="User not found",
                )

            if transaction.type not in ["deposit", "withdrawal"]:
                raise HTTPException(
                    status_code=422,
                    detail="Invalid transaction type",
                )

            if transaction.amount <= 0:
                raise HTTPException(
                    status_code=422,
                    detail="Amount must be greater than zero",
                )

            current_balance = float(user[0])

            if (
                transaction.type == "withdrawal"
                and transaction.amount > current_balance
            ):
                raise HTTPException(
                    status_code=400,
                    detail="Insufficient balance",
                )

            cursor.execute(
                """
                INSERT INTO transactions (user_id, amount, type)
                VALUES (%s, %s, %s)
                RETURNING id, user_id, amount, type, status, created_at
                """,
                (
                    transaction.user_id,
                    transaction.amount,
                    transaction.type,
                ),
            )

            new_transaction = cursor.fetchone()

            if transaction.type == "deposit":
                cursor.execute(
                    """
                    UPDATE users
                    SET balance = balance + %s
                    WHERE id = %s
                    """,
                    (transaction.amount, transaction.user_id),
                )
            else:
                cursor.execute(
                    """
                    UPDATE users
                    SET balance = balance - %s
                    WHERE id = %s
                    """,
                    (transaction.amount, transaction.user_id),
                )

            connection.commit()

            return {
                "id": new_transaction[0],
                "user_id": new_transaction[1],
                "amount": float(new_transaction[2]),
                "type": new_transaction[3],
                "status": new_transaction[4],
                "created_at": new_transaction[5],
            }

    finally:
        connection.close()

