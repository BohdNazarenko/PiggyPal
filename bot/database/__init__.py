from bot.database.db import DataBase
from bot.database.repositories.category import CategoryRepository
from bot.database.repositories.category_types import CategoryTypeRepository
from bot.database.repositories.debts import DebtRepository
from bot.database.repositories.expenses import ExpensesRepository
from bot.database.repositories.goals import GoalsRepository
from bot.database.repositories.incomes import IncomesRepository


def init_db():
    database = DataBase()
    CategoryTypeRepository(database).init_table()
    CategoryRepository(database).init_table()
    ExpensesRepository(database).init_table()
    IncomesRepository(database).init_table()
    DebtRepository(database).init_table()
    GoalsRepository(database).init_table()
