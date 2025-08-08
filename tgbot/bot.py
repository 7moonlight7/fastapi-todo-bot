from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
import asyncio
from config import BOT_TOKEN
from tgbot.handlers import user

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(user)


async def set_commands():
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="menu", description="Показать меню с задачами"),
        BotCommand(command="logout", description="Выйти из профиля"),
    ]
    await bot.set_my_commands(commands)


async def start_bot():
    await set_commands()
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        print('Бот запущен')
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass
