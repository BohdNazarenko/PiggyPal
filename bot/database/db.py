import psycopg2
from psycopg2.extras import DictCursor

DB_NAME = "piggy_pal_db"
DB_USER = "postgres"
DB_PASSWORD = "piggypal"
DB_HOST = "localhost"
DB_PORT = 5432


def connect_to_db():
    try:
        conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        print("Connected to database")
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        db_version = cursor.fetchone()
        print("Database version: %s " % db_version)
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None