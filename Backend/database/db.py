import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="siem_project",
        user="postgres",
        password="Darbi1234"
    )