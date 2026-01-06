import logging

from psycopg2 import DatabaseError

from bot.database import DataBase

logger = logging.getLogger(__name__)


class ExpensesRepository:
    def __init__(self, db: DataBase):
        self.db = db

    def init_table(self) -> None:
        drop_sql = "DROP TABLE IF EXISTS expenses CASCADE;"

        create_sql = """
        CREATE TABLE expenses (
            id          SERIAL PRIMARY KEY,
            user_id     BIGINT NOT NULL 
                        REFERENCES balance(user_id)
                        ON DELETE CASCADE,
            category_id INTEGER NOT NULL
                        REFERENCES categories(id)
                        ON DELETE RESTRICT
                        ON UPDATE CASCADE,
            amount      NUMERIC(10,2) NOT NULL,
            created_at  TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE INDEX IF NOT EXISTS idx_expenses_user_id ON expenses(user_id);
        """

        conn = self.db.connect_to_db()

        try:
            with conn.cursor() as cur:
                cur.execute(drop_sql)
                cur.execute(create_sql)
                conn.commit()
        except DatabaseError as e:
            conn.rollback()
            logger.error("Error creating expenses table", exc_info=e)
            raise
        finally:
            self.db.release_connection(conn)


    def add_expense(self, user_id: int, category_id: int, amount: float) -> int:


        insert_sql = """
        INSERT INTO expenses (user_id, category_id, amount)
        VALUES(%s, %s, %s)
        RETURNING expense_id;
        """

        conn = self.db.connect_to_db()

        try:
            with conn.cursor() as cur:
                cur.execute(insert_sql, (user_id, category_id, amount))
                new_id = cur.fetchone()[0]
                conn.commit()
            return new_id
        except DatabaseError:
            conn.rollback()
            raise
        finally:
            self.db.release_connection(conn)