import logging

from psycopg2 import DatabaseError

from bot.database import DataBase

logger = logging.getLogger(__name__)


class IncomesRepository:

    def __init__(self, db: DataBase):
        self.db = db


    def init_table(self) -> None:
        create_sql = """
        CREATE TABLE IF NOT EXISTS incomes (
            id          SERIAL PRIMARY KEY,
            user_id     BIGINT NOT NULL 
                        REFERENCES balance(user_id)
                        ON DELETE CASCADE,
            amount      NUMERIC(10, 2) NOT NULL,
            created_at  TIMESTAMPTZ DEFAULT NOW()
        );
        """

        index_sql = "CREATE INDEX IF NOT EXISTS idx_incomes_user_id ON incomes(user_id);"

        conn = self.db.connect_to_db()

        try:
            with conn.cursor() as cur:
                cur.execute(create_sql)
                cur.execute(index_sql)
                conn.commit()
        except DatabaseError as e:
            conn.rollback()
            logger.error("Error creating income table", exc_info=e)
            raise
        finally:
            self.db.release_connection(conn)

    def add_income(self, user_id: int, amount: float):

        insert_sql = """
        INSERT INTO incomes(user_id, amount)
        VALUES (%s, %s)
        RETURNING id;
        """

        conn = self.db.connect_to_db()

        try:
            with conn.cursor() as cur:
                cur.execute(insert_sql, (user_id, amount))
                new_id = cur.fetchone()[0]
                conn.commit()
            return new_id
        except DatabaseError as e:
            conn.rollback()
            logger.error("Error inserting income", exc_info=e)
            raise
        finally:
            self.db.release_connection(conn)