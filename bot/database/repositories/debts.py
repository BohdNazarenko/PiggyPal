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
        debt_id   SERIAL PRIMARY KEY,
         user_id         BIGINT  NOT NULL 
                        REFERENCES balance(user_id)
                        ON DELETE CASCADE,
        name      VARCHAR(25) NOT NULL,
        debt_count NUMERIC(10, 2)   NOT NULL,
        purpose     TEXT,
        create_at   TIMESTAMPTZ DEFAULT NOW()
    );
    """

        conn = self.db.connect_to_db()

        try:
            with conn.cursor() as cur:
                cur.execute(create_sql)
                conn.commit()
        except DatabaseError as e:
            logger.error("Error creating debts table", exc_info=e)
            raise
        finally:
            conn.close()

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
            conn.close()

    def add_debt(self, user_id: int, name: str, debt_count: float, purpose: str | None = None) -> int:

        insert_sql ="""
        INSERT INTO debts (user_id, name, debt_count, purpose)
        VALUES (%s, %s, %s, %s)
        RETURNING debt_id;
        """

        conn = self.db.connect_to_db()

        try:
            with conn.cursor() as cur:
                cur.execute(insert_sql, (user_id, name, debt_count, purpose))
                conn.commit()
                new_id = cur.fetchone()[0]
            logger.info("Inserted debt id=%d name=%s amount=%c.2f", new_id, name, debt_count)
            return new_id
        except DatabaseError as e:
            logger.error("Error inserting debt for '%s'", name, exc_info=e)
            raise
        finally:
            conn.close()
