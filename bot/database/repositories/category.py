from psycopg2.extras import RealDictCursor

from bot.database.db import DataBase


class CategoryRepository:

    def __init__(self, db: DataBase):
        self.db = db

    def init_table(self) -> None:
        create_sql = """
            CREATE TABLE IF NOT EXISTS categories(
                category_id   SERIAL PRIMARY KEY,
                category      VARCHAR(100) NOT NULL,
                category_type_id INTEGER   NOT NULL
                    REFERENCES categories_type(category_type_id)
                    ON DELETE RESTRICT
                    ON UPDATE CASCADE             
        );
        """

        initial_data = [
            # Food & Drink (type_id = 1)
            {"category": "Healthy Eating", "category_type_id": 1},
            {"category": "Fruits & Vegetables", "category_type_id": 1},
            {"category": "Water", "category_type_id": 1},
            {"category": "Dairy Products", "category_type_id": 1},
            {"category": "Drinks (Juices, Tea, Coffee)", "category_type_id": 1},

            # Harm to Health (type_id = 2)
            {"category": "Sweets & Pastries", "category_type_id": 2},
            {"category": "Unhealthy Drinks", "category_type_id": 2},
            {"category": "Energy Drinks", "category_type_id": 2},
            {"category": "Fast Food", "category_type_id": 2},
            {"category": "Alcohol & Tobacco", "category_type_id": 2},

            # Self-Improvement (type_id = 3)
            {"category": "Education & Courses", "category_type_id": 3},
            {"category": "Personal Care (Beauty & Health)", "category_type_id": 3},
            {"category": "Debts", "category_type_id": 3},

            # Lifestyle & Entertainment (type_id = 4)
            {"category": "Entertainment", "category_type_id": 4},
            {"category": "Clothing & Accessories", "category_type_id": 4},
            {"category": "Electronics", "category_type_id": 4},
            {"category": "Services", "category_type_id": 4},

            # House & Transport (type_id = 5)
            {"category": "House rent", "category_type_id": 5},
            {"category": "Household goods", "category_type_id": 5},
            {"category": "Transport", "category_type_id": 5},
        ]

        conn = self.db.connect_to_db()

        try:
            with conn.cursor() as cur:
                cur.execute(create_sql)
                cur.execute("SELECT COUNT(*) FROM categories;")
                count = cur.fetchone()[0]
                if count == 0:
                    insert_sql = """
                        INSERT INTO categories (category, category_type_id)
                        VALUES (%(category)s, %(category_type_id)s);                
                    """
                    cur.executemany(insert_sql, initial_data)
            conn.commit()
        finally:
            self.db.close()


    def list_by_type(self, type_id: int) -> list[dict]:

        sql_query = """
        SELECT  category_id,
                category,
                category_type_id
        FROM categories
        WHERE category_type_id = %s
        ORDER BY category_id
        """

        conn = self.db.connect_to_db()

        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql_query, (type_id,))
                return cur.fetchall()
        finally:
            conn.close()

