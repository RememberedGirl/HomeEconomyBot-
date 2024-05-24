import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import API_TOKEN
from handlers import handle_start, handle_help, handle_add_expense, handle_view_expenses
from db import init_db

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Регистрация обработчиков
dp.message.register(handle_start, commands=['start'])
dp.message.register(handle_help, commands=['help'])
dp.message.register(handle_add_expense, commands=['add_expense'])
dp.message.register(handle_view_expenses, commands=['view_expenses'])

async def on_startup(dispatcher):
    await init_db()

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, on_startup=on_startup)
