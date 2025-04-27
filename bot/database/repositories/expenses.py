from psycopg2 import DatabaseError

from bot.database import DataBase


class ExpensesRepository:
    def __init__(self, db: DataBase):
        self.db = db

    def init_table(self) -> None:

        create_sql = """
        CREATE TABLE IF NOT EXISTS expenses (
        expense_id      SERIAL PRIMARY KEY,
        category_id     INTEGER NOT NULL
            REFERENCES categories(category_id)
            ON DELETE RESTRICT
            ON UPDATE CASCADE,
        amount          NUMERIC(10,2) NOT NULL,
        created_at      TIMESTAMP DEFAULT NOW()
        );
        """


        conn = self.db.connect_to_db()

        try:
            with conn.cursor() as cur:
                cur.execute(create_sql)
                conn.commit()
        except DatabaseError as e:
            conn.rollback()
            print(f"Error creating expenses table: {e}")
            raise
        finally:
            conn.close()