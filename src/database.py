import psycopg


DATABASE_URL = (
    "host=localhost "
    "port=5432 "
    "dbname=finflow "
    "user=finflow "
    "password=finflow_password"
)


def get_connection():
    return psycopg.connect(DATABASE_URL)