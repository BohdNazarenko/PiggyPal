from psycopg2.extras import RealDictCursor

from bot.database import DataBase


class CategoryTypeRepository:

    def __init__(self, db: DataBase):
        self.db = db

    def init_table(self) -> None:
        create_sql = """
        CREATE TABLE IF NOT EXISTS category_types (
            id          SERIAL PRIMARY KEY,
            name        VARCHAR(100) NOT NULL,
            description TEXT
        );
        """

        initial_data = [
            {"name": "Food & Drink", "description": "Groceries, beverages, dining out"},
            {"name": "Harm to Health", "description": "Alcohol, tobacco, fast food, sweets"},
            {"name": "Self-Improvement", "description": "Education, personal care, debt repayment"},
            {"name": "Lifestyle & Entertainment", "description": "Recreation, fashion, gadgets, services"},
            {"name": "House & Transport", "description": "Rent, home goods, commuting"},
        ]

        conn = self.db.connect_to_db()
        try:
            with conn.cursor() as cur:
                cur.execute(create_sql)
                cur.execute("SELECT COUNT(*) FROM category_types")
                count = cur.fetchone()[0]
                if count == 0:
                    insert_sql = """
                        INSERT INTO category_types (name, description)
                        VALUES (%(name)s, %(description)s);
                    """
                    cur.executemany(insert_sql, initial_data)
            conn.commit()
        finally:
            self.db.release_connection(conn)

    def list_all(self) -> list[dict]:

        sql_query = """
        SELECT  id AS category_type_id,
                name AS category_type,
                description
        FROM category_types
        ORDER BY id;
        """

        conn = self.db.connect_to_db()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql_query)
                return cur.fetchall()
        finally:
            self.db.release_connection(conn)
