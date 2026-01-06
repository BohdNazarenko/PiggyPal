import logging

from psycopg2 import DatabaseError

from bot.database import DataBase

logger = logging.getLogger(__name__)


class GoalRepository:

    def __init__(self, db: DataBase):
        self.db = db

    def init_table(self) -> None:
        drop_sql = "DROP TABLE IF EXISTS goals CASCADE;"

        create_sql = """
        CREATE TABLE goals (
            goal_id     SERIAL PRIMARY KEY,
            user_id     BIGINT NOT NULL 
                        REFERENCES balance(user_id)
                        ON DELETE CASCADE, 
            name        VARCHAR(100) NOT NULL,
            price       NUMERIC(10, 2) NOT NULL,
            description TEXT,
            created_at  TIMESTAMPTZ DEFAULT NOW()
        );
        """

        conn = self.db.connect_to_db()

        try:
            with conn.cursor() as cur:
                cur.execute(drop_sql)
                cur.execute(create_sql)
                conn.commit()
        except DatabaseError as e:
            conn.rollback()
            logger.error("Error creating goals table", exc_info=e)
            raise
        finally:
            self.db.release_connection(conn)

    def add_goal(self, user_id: int, name: str, price: float, description: str | None = None) -> int:

        sql_insert = """
        INSERT INTO goals (user_id, name, price, description)
        VALUES (%s, %s, %s, %s)
        RETURNING goal_id;
        """

        conn = self.db.connect_to_db()

        try:
            with conn.cursor() as cur:
                cur.execute(sql_insert, (user_id, name, price, description))
                new_id = cur.fetchone()[0]
                conn.commit()
                return new_id
        except DatabaseError as e:
            conn.rollback()
            logger.error("Error inserting goal", exc_info=e)
            raise
        finally:
            self.db.release_connection(conn)