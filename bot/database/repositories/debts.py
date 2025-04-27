from psycopg2 import DatabaseError
from sqlalchemy.dialects.postgresql import psycopg2

from bot.database import DataBase


class DebtRepository:

    def __init__(self, db: DataBase):
        self.db = db

    def init_table(self):

        create_sql = """
    CREATE TABLE IF NOT EXISTS debts (
        debt_id   SERIAL PRIMARY KEY,
        name      VARCHAR(25) NOT NULL,
        debt_count NUMERIC(10, 2)   NOT NULL,
        purpose     TEXT,
        create_at   TIMESTAMP DEFAULT NOW()
    );
    """

        conn = self.db.connect_to_db()

        try:
            with conn.cursor() as cur:
                cur.execute(create_sql)
                conn.commit()
        except DatabaseError as e:
            conn.rollback()
            print(f"Error creating debts table: {e}")
            raise
        finally:
            conn.close()
