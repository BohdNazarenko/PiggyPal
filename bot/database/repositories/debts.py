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

    def list_debtors(self) -> list[str]:

        sql_query = """
        SELECT DISTINCT name
        FROM debts
        ORDER BY name
        """

        conn = self.db.connect_to_db()

        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql_query)
                return [row["name"] for row in cur.fetchall()]
        finally:
            conn.close()

    def add_debt(self, name: str, debt_count: float, purpose: str | None = None) -> int:

        insert_sql ="""
        INSERT INTO debts (name, debt_count, purpose)
        VALUES (%s, %s, %s)
        RETURNING debt_id;
        """

        conn = self.db.connect_to_db()

        try:
            with conn.cursor() as cur:
                cur.execute(insert_sql, (name, debt_count, purpose))
                conn.commit()
                new_id = cur.fetchone()[0]
            logger.info("Inserted debt id=%d name=%s amount=%.2f", new_id, name, debt_count)
            return new_id
        except DatabaseError as e:
            logger.error("Error inserting debt for '%s'", name, exc_info=e)
            raise
        finally:
            conn.close()
