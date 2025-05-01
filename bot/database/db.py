import psycopg2
from psycopg2.extras import RealDictCursor

from config.settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


class DataBase:

    def __init__(self):
        self._conn = None

    def connect_to_db(self):
        if self._conn is None or self._conn.closed:
            self._conn = psycopg2.connect(
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
            )
        return self._conn

    def close(self):
        if self._conn and not self._conn.closed:
            self._conn.close()
            self._conn = None

    def cursor(self, dict_cursor: bool = False):
        conn = self.connect_to_db()
        if dict_cursor:
            return conn.cursor(cursor_factory=RealDictCursor)
        return conn.cursor()

    def __enter__(self, ext_type, exc, tb):
        return self

    def __exit__(self):
        self.close()
