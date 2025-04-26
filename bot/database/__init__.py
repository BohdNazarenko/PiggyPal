from bot.database.db import DataBase
from bot.database.repositories.category import CategoryRepository
from bot.database.repositories.category_types import CategoryTypeRepository


def init_db():
    db = DataBase()

    CategoryRepository(db).init_table()

    CategoryTypeRepository(db).init_table()