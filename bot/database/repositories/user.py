import logging

from psycopg2 import DatabaseError
from psycopg2.extras import RealDictCursor

from bot.database.db import DataBase

logger = logging.getLogger(__name__)


class UserRepository:

    def __init__(self, db: DataBase):
        self.db = db

    def init_table(self) -> None:
        drop_sql = "DROP TABLE IF EXISTS users CASCADE;"

        create_sql = """
        CREATE TABLE users (
            id          BIGINT PRIMARY KEY,
            username    VARCHAR(255),
            first_name  VARCHAR(255),
            last_name   VARCHAR(255),
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
            logger.error("Error creating users table", exc_info=e)
            raise
        finally:
            self.db.release_connection(conn)

    def get_or_create(self, user_id: int, username: str | None = None,
                      first_name: str | None = None, last_name: str | None = None) -> dict:
        """Get existing user or create new one."""

        upsert_sql = """
        INSERT INTO users (id, username, first_name, last_name)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            username = COALESCE(EXCLUDED.username, users.username),
            first_name = COALESCE(EXCLUDED.first_name, users.first_name),
            last_name = COALESCE(EXCLUDED.last_name, users.last_name)
        RETURNING id, username, first_name, last_name, created_at;
        """

        conn = self.db.connect_to_db()

        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(upsert_sql, (user_id, username, first_name, last_name))
                user = cur.fetchone()
                conn.commit()
                return dict(user)
        except DatabaseError as e:
            conn.rollback()
            logger.error("Error upserting user", exc_info=e)
            raise
        finally:
            self.db.release_connection(conn)

    def get_by_id(self, user_id: int) -> dict | None:
        sql_query = """
        SELECT id, username, first_name, last_name, created_at
        FROM users
        WHERE id = %s;
        """

        conn = self.db.connect_to_db()

        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql_query, (user_id,))
                row = cur.fetchone()
                return dict(row) if row else None
        finally:
            self.db.release_connection(conn)

