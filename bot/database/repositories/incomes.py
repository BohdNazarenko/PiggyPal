from psycopg2 import DatabaseError, connect

from bot.database import DataBase


class IncomesRepository:

    def __init__(self, db: DataBase):
        self.db = db


    def init_table(self) -> None:

        create_sql = """
        CREATE TABLE IF NOT EXISTS incomes (
        income_id   SERIAL PRIMARY KEY,
        user_id     BIGINT  NOT NULL 
                    REFERENCES balance(user_id)
                    ON DELETE CASCADE,
        amount      NUMERIC(10, 2) NOT NULL,
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
            print(f"Error creating income table: {e}")
            raise
        finally:
            conn.close()

    def add_income(self, user_id: int, amount: float):

        insert_sql = """
        INSERT INTO incomes(user_id, amount)
        VALUES (%s, %s)
        RETURNING income_id;
        """

        conn = self.db.connect_to_db()

        try:
            with conn.cursor() as cur:
                cur.execute(insert_sql, (user_id, amount))
                new_id = cur.fetchone()[0]
                conn.commit()
            return new_id
        except DatabaseError as e:
            print(f"Error inserting income: {e}")
            raise
        finally:
            conn.close()