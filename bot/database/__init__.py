from bot.database.db import DataBase
from bot.database.repositories.user import UserRepository
from bot.database.repositories.balance import BalanceRepository
from bot.database.repositories.category import CategoryRepository
from bot.database.repositories.category_types import CategoryTypeRepository
from bot.database.repositories.debt import DebtRepository
from bot.database.repositories.expenses import ExpensesRepository
from bot.database.repositories.goal import GoalRepository
from bot.database.repositories.incomes import IncomesRepository


def init_db():
    database = DataBase()
    # Order matters! Parent tables first.
    UserRepository(database).init_table()      # users first (parent)
    BalanceRepository(database).init_table()   # balance references users
    CategoryTypeRepository(database).init_table()
    CategoryRepository(database).init_table()  # categories references category_types
    ExpensesRepository(database).init_table()  # expenses references balance, categories
    IncomesRepository(database).init_table()   # incomes references balance
    DebtRepository(database).init_table()      # debts references balance
    GoalRepository(database).init_table()      # goals references balance
