# PiggyPal
A Financial Expense Tracker Telegram Bot

Концепция бота:
Мой бот будет помогать отслеживать личные финансы, позволяя пользователю вводить доходы и расходы, 
категоризировать их и получать аналитику.


Возможности бота:
1)  Добавление расходов и доходов через команды в Telegram.
2)  Категоризация трат: По ключевым словам бот сможет автоматически относить траты к определённым категориям 
    (например, "еда", "транспорт").
3)  Хранение данных в PostgreSQL: Это позволит сохранять историю расходов и доходов, которые потом можно анализировать.
4)  Анализ данных: Бот может подсчитывать ежемесячные расходы, показывать траты по категориям и строить прогнозы на 
    основе предыдущих месяцев.
5)  Визуализация: В будущем можно будет добавить генерацию графиков расходов, которые бот будет отправлять 
    в виде изображений.


Описание пользовательских сценариев:
1) Сценарий первого входа: Пользователь регистрируется в боте, также указывая своё нынешнее финансовое состояние.
2) Сценарий добавления траты/дохода: Пользователь нажимает на кнопку или пишет команду 
   /add_expense 100 food | /add_income 1000 job, бот записывает эту трату и подтверждает её сохранение.
3) Сценарий возможности добавления пользовательской категории: Пользователь может добавить свою категорию, 
   которая автоматически заполниться в табличке базы данных
4) Сценарий возвращение таблицы разходов/доходов: Пользователь нажимает на кнопку либо отправляет команду 
   /report, и бот возвращает текстовый отчёт за выбранный период.
5) Сценарий добавления чека: Пользователь добавляет фотографию чека, фотография сохраняется в бд, 
   после чего пользователь сможет кнопкой либо командой /take_all_active_payments вписать в бот, а после 
   команды /done✅ бот удаляет фотографию чека из бд (в будущем ии сам будет обрабатовать чек).

Структура и наполнение таблиц
categories — действия пользователей с заказами. 



