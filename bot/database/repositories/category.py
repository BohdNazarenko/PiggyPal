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
            {"category": "Healthy Groceries", "category_type_id": 1},
            {"category": "Dairy & Eggs", "category_type_id": 1},
            {"category": "Health & Personal Care", "category_type_id": 2},
            {"category": "Utilities & Communication", "category_type_id": 5},
            {"category": "Self-development", "category_type_id": 4},
            {"category": "Debts", "category_type_id": 4},
            {"category": "Sugary & Soft Drinks", "category_type_id": 1},
            {"category": "Sweets", "category_type_id": 3},
            {"category": "Entertainment", "category_type_id": 6},
            {"category": "Household Goods", "category_type_id": 5},
            {"category": "Transportation", "category_type_id": 7},
            {"category": "Clothing", "category_type_id": 6},
            {"category": "Electronics", "category_type_id": 7},
            {"category": "Takeout & Fast Food", "category_type_id": 3},
            {"category": "Alcohol", "category_type_id": 3},
            {"category": "Nicotine", "category_type_id": 3},
            {"category": "Energy Drinks", "category_type_id": 3},
            {"category": "Medicine", "category_type_id": 2},
            {"category": "Sports", "category_type_id": 2},
            {"category": "Salary", "category_type_id": 2},
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
