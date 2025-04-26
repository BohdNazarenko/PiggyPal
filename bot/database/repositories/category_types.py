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
            {"category_type": "Food & Drink", "description": "Groceries, drinks, meals"},
            {"category_type": "Personal Care", "description": "Personal care, medicine, doctor visits, sports"},
            {"category_type": "Harm to health", "description": "Alcohol, nicotine, fast food, energy drinks, sweets"},
            {"category_type": "Self-Improvement", "description": "Education, debts, donations"},
            {"category_type": "Necessary expenses",
             "description": "Rent, home interior, loans, debts, financial commitments"},
            {"category_type": "Entertainment and clothing", "description": "Leisure activities, clothing"},
            {"category_type": "Transport & Technology", "description": "Transport, electronics, communication"},
            {"category_type": "Money incomes", "description": "Salary, all money income methods"},
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
            self.db.close()
