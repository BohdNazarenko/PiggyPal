from psycopg2.extras import RealDictCursor

from bot.database.db import DataBase


class CategoryRepository:

    def __init__(self, db: DataBase):
        self.db = db

    def init_table(self) -> None:
        create_sql = """
        CREATE TABLE IF NOT EXISTS categories (
            id              SERIAL PRIMARY KEY,
            name            VARCHAR(100) NOT NULL,
            category_type_id INTEGER NOT NULL
                            REFERENCES category_types(id)
                            ON DELETE RESTRICT
                            ON UPDATE CASCADE             
        );
        """

        initial_data = [
            # Food & Drink (type_id = 1)
            {"name": "Healthy Eating", "type_id": 1},
            {"name": "Fruits & Vegetables", "type_id": 1},
            {"name": "Water", "type_id": 1},
            {"name": "Dairy Products", "type_id": 1},
            {"name": "Drinks (Juices, Tea, Coffee)", "type_id": 1},

            # Harm to Health (type_id = 2)
            {"name": "Sweets & Pastries", "type_id": 2},
            {"name": "Unhealthy Drinks", "type_id": 2},
            {"name": "Energy Drinks", "type_id": 2},
            {"name": "Fast Food", "type_id": 2},
            {"name": "Alcohol & Tobacco", "type_id": 2},

            # Self-Improvement (type_id = 3)
            {"name": "Education & Courses", "type_id": 3},
            {"name": "Personal Care (Beauty & Health)", "type_id": 3},
            {"name": "Debts", "type_id": 3},

            # Lifestyle & Entertainment (type_id = 4)
            {"name": "Entertainment", "type_id": 4},
            {"name": "Clothing & Accessories", "type_id": 4},
            {"name": "Electronics", "type_id": 4},
            {"name": "Services", "type_id": 4},

            # House & Transport (type_id = 5)
            {"name": "House rent", "type_id": 5},
            {"name": "Household goods", "type_id": 5},
            {"name": "Transport", "type_id": 5},
        ]

        conn = self.db.connect_to_db()

        try:
            with conn.cursor() as cur:
                cur.execute(create_sql)
                cur.execute("SELECT COUNT(*) FROM categories")
                count = cur.fetchone()[0]
                if count == 0:
                    insert_sql = """
                        INSERT INTO categories (name, category_type_id)
                        VALUES (%(name)s, %(type_id)s);                
                    """
                    cur.executemany(insert_sql, initial_data)
            conn.commit()
        finally:
            self.db.release_connection(conn)


    def list_by_type(self, type_id: int) -> list[dict]:

        sql_query = """
        SELECT  id AS category_id,
                name AS category,
                category_type_id
        FROM categories
        WHERE category_type_id = %s
        ORDER BY id
        """

        conn = self.db.connect_to_db()

        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql_query, (type_id,))
                return cur.fetchall()
        finally:
            self.db.release_connection(conn)

