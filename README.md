# FastAPI ToDoBot - Task Manager with Telegram Integration

<p align="center">
  <img src="https://miro.medium.com/v2/resize:fit:614/1*0sQg0SQlFZvAviQWywTiow.png" alt="banner" />
</p>


[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=blue)](https://docs.python.org/3.13/)
[![Aiogram](https://img.shields.io/badge/Aiogram-python-blue?logo=python&logoColor=blue)](https://github.com/aiogram/aiogram)
[![FastAPI](https://img.shields.io/badge/FastAPI-python-blue?logo=fastapi&logoColor=blue)](https://github.com/fastapi/fastapi)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-python-blue?logo=SQLAlchemy&logoColor=blue)](https://github.com/sqlalchemy/sqlalchemy)
[![MIT](https://img.shields.io/badge/License-MIT-blue)]()
[![Telegram](https://img.shields.io/badge/telegram-chat-blue?logo=telegram&logoColor=blue)](https://t.me/hamoonlightte)

### This `Telegram bot` is designed to help users efficiently manage their daily tasks and to-do lists directly within the Telegram messenger. It leverages the power of the Aiogram library for seamless interaction with the Telegram Bot API, combined with a [FastAPI](https://github.com/fastapi/fastapi) backend and [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) for reliable and scalable data management.

## ✨ Features

1. 🔐 User authentication (login required)
2. ➕🗑️✏️👀 Add, delete, update, and view tasks
3. 💾 Persistent storage using SQLAlchemy and SQLite
4. 🤖 Bot interaction powered by Aiogram
5. ⚙️ REST API backend with FastAPI

## ⚙️ Installation

### 1. Make sure you have **Python 3.7+** installed.

### 2. Clone the repository

```bash
git clone https://github.com/7moonlight7/fastapi-todo-bot.git
cd todolist
```

### 3. Install required dependencies.

It is recommended to use a virtual environment:

```bash
python -m venv venv 
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 4. Running the Application

To run the application, you need to start both the Telegram bot and the FastAPI server.

- In one terminal, run the Telegram bot with:

```bash
python -m tgbot.bot
```

- In another terminal, start the FastAPI server with:

```bash
uvicorn main:app --reload
```

This way, the bot will handle Telegram interactions while the FastAPI server provides the backend API.

## 📂 Project Structure

```
todolist/
├── .venv/                 # Virtual environment folder
├── database/              # Database setup and models
│   │   ├── database.py    # Database connection and engine setup (SQLAlchemy)
│   │   ├── models.py      # ORM models for User and Task tables 
├── tgbot/                 # Telegram bot source code
│   ├── keyboards/         # Bot keyboards 
│   │   ├── __init__.py   
│   │   ├── inline.py      # Inline buttons
│   ├── __init__.py
│   ├── bot.py             # Main bot logic
│   ├── handlers.py        # Handlers for Telegram bot commands
│   ├── states.py          # Bot states for FSM
├── config.py              # Configuration settings
├── LICENSE.md
├── main.py                # FastAPI application entrypoint
├── pydantic_model.py      # Pydantic schemas
├── README.md
└── requirements.txt       # Project dependencies list
```

## 📋 Usage Notes

1. 🔐 You need to log into your account in the bot to manage tasks.
2. ✅ Once logged in, you can:
    1. ➕ Add new tasks.
    2. 🗑️ Delete existing tasks.
    3. ✏️ Update task details.
    4. 📋 View your list of tasks.
3. 💾 All changes are saved in the database for persistence.

## 🗄️ Database

The application uses `SQLite` for persistent storage, managed via `SQLAlchemy ORM`.

The database engine is created with:

```
engine = create_engine('sqlite:///user.db', echo=True)
```

This means the SQLite database file user.db is created and stored in the root directory of the project.

All users and their tasks are stored in this database.
There are two main models:

- User — represents a user account.
- Task — represents a task associated with a specific user.

Each task is linked to a user, ensuring that tasks are private and managed per account.

This setup allows efficient querying and management of user-specific tasks through SQLAlchemy.

## License

Distributed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Contact

- 💬 Telegram: [@hamoonlightte](https://t.me/hamoonlightte) 
