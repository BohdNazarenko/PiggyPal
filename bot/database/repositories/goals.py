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
            print(f"Error creating goals table: {e}")
            raise
        finally:
            conn.close()

    def add_goal(self, stuff_name: str, price: float, desc: str | None = None) -> int:

        sql_insert = """
        INSERT INTO goals (stuff_name, price, description)
        VALUES (%s, %s, %s)
        RETURNING goal_id;
        """

        conn = self.db.connect_to_db()

        try:
            with conn.cursor() as cur:
                cur.execute(sql_insert, (stuff_name, price, desc))
                conn.commit()
                return cur.fetchone()[0]
        except ValueError as e:
            print(f"Error inserting goal: {e}")
            raise
        finally:
            conn.close()