import psycopg

from src.database import DATABASE_URL


def test_database_connection():
    connection = psycopg.connect(DATABASE_URL)

    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

    connection.close()

    assert result[0] == 1


def test_users_table_exists():
    connection = psycopg.connect(DATABASE_URL)

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = 'users'
            )
            """
        )

        result = cursor.fetchone()

    connection.close()

    assert result[0] is True


def test_transactions_table_exists():
    connection = psycopg.connect(DATABASE_URL)

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = 'transactions'
            )
            """
        )

        result = cursor.fetchone()

    connection.close()

    assert result[0] is True