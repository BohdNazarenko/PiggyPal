import logging

from psycopg2 import DatabaseError
from psycopg2.extras import RealDictCursor

from bot.database import DataBase

logger = logging.getLogger(__name__)

class DebtRepository:

    def __init__(self, db: DataBase):
        self.db = db

    def init_table(self) -> None:
        create_sql = """
        CREATE TABLE IF NOT EXISTS debts (
            id          SERIAL PRIMARY KEY,
            user_id     BIGINT NOT NULL 
                        REFERENCES balance(user_id)
                        ON DELETE CASCADE,
            name        VARCHAR(100) NOT NULL,
            amount      NUMERIC(10, 2) NOT NULL,
            purpose     TEXT,
            created_at  TIMESTAMPTZ DEFAULT NOW()
        );
        """

        index_sql = "CREATE INDEX IF NOT EXISTS idx_debts_user_id ON debts(user_id);"

        conn = self.db.connect_to_db()

        try:
            with conn.cursor() as cur:
                cur.execute(create_sql)
                cur.execute(index_sql)
                conn.commit()
        except DatabaseError as e:
            conn.rollback()
            logger.error("Error creating debts table", exc_info=e)
            raise
        finally:
            self.db.release_connection(conn)

    def list_debtors(self, user_id) -> list[str]:

        sql_query = """
        SELECT DISTINCT name
        FROM debts
        WHERE user_id = %s
        ORDER BY name
        """

        conn = self.db.connect_to_db()

        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql_query, (user_id,))
                return [row["name"] for row in cur.fetchall()]
        finally:
            self.db.release_connection(conn)

    def add_debt(self, user_id: int, name: str, amount: float, purpose: str | None = None) -> int:

        insert_sql = """
        INSERT INTO debts (user_id, name, amount, purpose)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """

        conn = self.db.connect_to_db()

        try:
            with conn.cursor() as cur:
                cur.execute(insert_sql, (user_id, name, amount, purpose))
                new_id = cur.fetchone()[0]
                conn.commit()
            logger.info("Inserted debt id=%d name=%s amount=%.2f", new_id, name, amount)
            return new_id
        except DatabaseError as e:
            conn.rollback()
            logger.error("Error inserting debt for '%s'", name, exc_info=e)
            raise
        finally:
            self.db.release_connection(conn)
