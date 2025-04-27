from psycopg2 import DatabaseError
from bot.database import DataBase


class GoalsRepository:

    def __init__(self, db: DataBase):
        self.db = db

    def init_table(self) -> None:
        create_sql = """
        CREATE TABLE IF NOT EXISTS goals (
        goal_id     SERIAL PRIMARY KEY,
        stuff_name  VARCHAR(25) NOT NULL,
        price       NUMERIC(10, 2) NOT NULL,
        description TEXT,
        created_at  TIMESTAMP DEFAULT NOW()
        );
        """

        conn = self.db.connect_to_db()

        try:
            with conn.cursor() as cur:
                cur.execute(create_sql)
                conn.commit()
        except DatabaseError as e:
            conn.rollback()
            print(f"Error creating goals table: {e}")
            raise
        finally:
            conn.close()
