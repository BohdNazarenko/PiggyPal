import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor

from config.settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


class DataBase:
    """Database connection manager with connection pooling."""

    _pool: pool.SimpleConnectionPool | None = None

    @classmethod
    def _get_pool(cls) -> pool.SimpleConnectionPool:
        """Lazy initialization of connection pool (singleton)."""
        if cls._pool is None:
            cls._pool = pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
            )
        return cls._pool

    def connect_to_db(self):
        """Get a connection from the pool."""
        return self._get_pool().getconn()

    def release_connection(self, conn):
        """Return a connection back to the pool."""
        if conn and self._pool:
            self._pool.putconn(conn)

    @classmethod
    def close_pool(cls):
        """Close all connections in the pool (call on app shutdown)."""
        if cls._pool:
            cls._pool.closeall()
            cls._pool = None

    def cursor(self, dict_cursor: bool = False):
        conn = self.connect_to_db()
        if dict_cursor:
            return conn.cursor(cursor_factory=RealDictCursor)
        return conn.cursor()

    def __enter__(self):
        self._conn = self.connect_to_db()
        return self._conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._conn:
            if exc_type is None:
                self._conn.commit()
            else:
                self._conn.rollback()
            self.release_connection(self._conn)
            self._conn = None
        return False
