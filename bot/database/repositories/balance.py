from psycopg2.extras import RealDictCursor


class BalanceRepository:

    def __init__(self, db):
        self.db = db

    def init_table(self) -> None:
        create_sql = """
        CREATE TABLE IF NOT EXISTS balance (
        balance_id      SERIAL PRIMARY KEY,
        user_id         BIGINT NOT NULL UNIQUE,
        current_balance NUMERIC(14,2) NOT NULL DEFAULT 0
        );
        """

        conn = self.db.connect_to_db()

        try:
            with conn.cursor() as cur:
                cur.execute(create_sql)
                conn.commit()
        finally:
            self.db.release_connection(conn)

    def get_balance(self, user_id: int) -> float:

        sql_select = """
        SELECT current_balance FROM balance WHERE user_id = %s;
        """

        conn = self.db.connect_to_db()

        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql_select, (user_id,))
                row = cur.fetchone()
                return float(row["current_balance"]) if row else 0.00
        finally:
            self.db.release_connection(conn)

    def set_balance(self, user_id: int, current_balance: float) -> None:

        insert_sql = """
        INSERT INTO balance(user_id, current_balance)
        VALUES (%s, %s)
        ON CONFLICT(user_id) DO UPDATE SET current_balance = EXCLUDED.current_balance;
        """

        conn = self.db.connect_to_db()

        try:
            with conn.cursor() as cur:
                cur.execute(insert_sql, (user_id, current_balance))
                conn.commit()
        finally:
            self.db.release_connection(conn)


    def update_balance(self, user_id: int, delta: float) -> float:

        current = self.get_balance(user_id)
        new_balance = current + delta
        self.set_balance(user_id, new_balance)
        return new_balance
