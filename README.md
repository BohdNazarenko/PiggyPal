# 🐷 PiggyPal – Your Personal Expense Tracker Bot


PiggyPal is a **Telegram bot** that helps users _track daily expenses_, categorize spending, and stay financially aware
all through a simple and friendly interface. Built with Python and PostgreSQL, this project demonstrates a clean, 
modular architecture and bot development skills.

## 🚀 Features

    📥 Add and categorize expenses via Telegram
    
    📊 View summaries by date and category
    
    🧠 Persistent storage with PostgreSQL
    
    ⚙️ Modular architecture for easy scaling and testing
    
    🔐 Secure configuration with .env support
    
    🐳 Docker-based setup for quick deployment

## 🛠️ Tech Stack

| Layer            | Tools & Technologies                                                                 |
|------------------|----------------------------------------------------------------------------------------|
| **Bot Engine**   | `pyTelegramBotAPI` (core bot framework)                                               |
| **Backend**      | `Python 3.10+`, `PostgreSQL`                                                          |
| **Database/ORM** | `psycopg2-binary` (PostgreSQL driver), raw SQL, `SQLAlchemy`                          |
| **Data Handling**| `pandas`, `numpy`                                                                     |
| **Configuration**| `.env`, `python-dotenv`, `config.py`                                                  |
| **Security**     | `cryptography`, `pyOpenSSL`, `PySocks`                                                |
| **Logging**      | Python `logging` module                                                               |
| **DevOps**       | `Docker`, `docker-compose`                                                            |
| **Testing**      | `pytest`, `unittest` (planned)                                                        |
| **Packaging**    | `pip`, `setuptools`, `filelock`, `typing_extensions`, `packaging`, `attrs`            |
| **Others**       | `Pygments`, `more-itertools`, `zipp`, `protobuf`                                      |


## 📁 Project Structure

    PiggyPal/
    ├── bot/
    │   ├── main.py
    │   ├── handlers/
    │   ├── keyboards/
    │   ├── middlewares/
    │   ├── utils/
    │   └── database/
    ├── config/    <- must to be added .env with secure configuration for project
    │   └── settings.py   
    ├── tests/
    │   └── test_main.py
    ├── logs/
    │   └── bot.log
    ├── docker-compose.yml
    ├── requirements.txt
    └── README.md

## Quickstart with Docker

1.	Build the image

`docker build -t piggy_postgres .`

2. Run the container

`docker run -d --name piggy_postgres \
  -p 5432:5432 \
  -e POSTGRES_USER=money \
  -e POSTGRES_PASSWORD=cash \
  -e POSTGRES_DB=piggy_db \
  -v pgdata:/var/lib/postgresql/data \
  piggy_postgres`

3. Run the bot

`python bot/main.py`


## ⚙️ Environment Variables

Create a .env file in the project root:

    BOT_TOKEN=your_telegram_bot_token
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=piggy_db
    DB_USER=money
    DB_PASSWORD=cash

### This version is fully functional and ready to demo. Future improvements may include:

	•	Income tracking
	•	Monthly budget goals
	•	Data export to CSV
	•	Admin dashboard (e.g. with Dash or FastAPI)

## 👨‍💻 Author

Bohdan Nazarenko

[GitHub](https://github.com/BohdNazarenko) • [LinkedIn](https://www.linkedin.com/in/bohdan-nazarenko-2akad605b2/)







