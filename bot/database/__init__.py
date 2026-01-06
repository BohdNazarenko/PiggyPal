from bot.database.db import DataBase
from bot.database.repositories.balance import BalanceRepository
from bot.database.repositories.category import CategoryRepository
from bot.database.repositories.category_types import CategoryTypeRepository
from bot.database.repositories.debt import DebtRepository
from bot.database.repositories.expenses import ExpensesRepository
from bot.database.repositories.goal import GoalRepository
from bot.database.repositories.incomes import IncomesRepository


def init_db():
    database = DataBase()
    BalanceRepository(database).init_table()
    CategoryTypeRepository(database).init_table()
    CategoryRepository(database).init_table()
    ExpensesRepository(database).init_table()
    IncomesRepository(database).init_table()
    DebtRepository(database).init_table()
    GoalRepository(database).init_table()
