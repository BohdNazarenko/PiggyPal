from psycopg2.extras import RealDictCursor

from bot.database import DataBase


class CategoryTypeRepository:

    def __init__(self, db: DataBase):
        self.db = db

    def init_table(self) -> None:
        create_sql = """
        CREATE TABLE IF NOT EXISTS categories_type (
            category_type_id  SERIAL PRIMARY KEY,
            category_type     VARCHAR(100)   NOT NULL,
            description       TEXT
            );
        """

        initial_data = [
            {"category_type": "Food & Drink", "description": "Groceries, beverages, dining out"},
            {"category_type": "Harm to Health", "description": "Alcohol, tobacco, fast food, sweets"},
            {"category_type": "Self-Improvement", "description": "Education, personal care, debt repayment"},
            {"category_type": "Lifestyle & Entertainment", "description": "Recreation, fashion, gadgets, services"},
            {"category_type": "House & Transport", "description": "Rent, home goods, commuting"},
        ]

        conn = self.db.connect_to_db()
        try:
            with conn.cursor() as cur:
                cur.execute(create_sql)
                cur.execute("SELECT COUNT(*) FROM categories_type")
                count = cur.fetchone()[0]
                if count == 0:
                    insert_sql = """
                        INSERT INTO categories_type (category_type, description)
                        VALUES (%(category_type)s, %(description)s);
                    """
                    cur.executemany(insert_sql, initial_data)
            conn.commit()
        finally:
            self.db.release_connection(conn)

    def list_all(self) -> list[dict]:

        sql_query = """
        SELECT  category_type_id,
                category_type,
                description
        FROM categories_type
        ORDER BY category_type_id;
        """

        conn = self.db.connect_to_db()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql_query)
                return cur.fetchall()
        finally:
            self.db.release_connection(conn)
