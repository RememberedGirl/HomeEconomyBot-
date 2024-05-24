import logging
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import API_TOKEN, USER_ID
from db.database import add_user, get_user

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot) #класс обработки входящих событий
scheduler = AsyncIOScheduler()


@dp.message(Command('start'))
async def start_handler(message: types.Message):
    chat_id = message.chat.id

    # Проверяем, зарегистрирован ли уже пользователь
    user = await get_user(chat_id)

    if user:
        await message.answer("Вы уже зарегистрированы в системе.")
    else:
        # Добавляем пользователя в базу данных
        await add_user(chat_id)
        await message.answer("Вы успешно зарегистрированы в системе.")

def ger_recent_event():
    return "ееее"

async def send_event(bot: Bot):
    event_list = ger_recent_event()
    await bot.send_message(USER_ID, f"спам {event_list}")

async def main():
    scheduler.add_job(send_event, "interval", seconds=10, args=(bot,))
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    print("start")
    asyncio.run(main())
