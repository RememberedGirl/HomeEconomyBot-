import logging
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import API_TOKEN, USER_ID
from db.database import add_user, get_user, add_category, add_expense

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


class AddCategory(StatesGroup):
    waiting_for_category_name = State()

class AddExpense(StatesGroup):
    waiting_for_date = State()
    waiting_for_price = State()
    waiting_for_category = State()

@dp.message(Command('addcategory'))
async def add_category_handler(message: types.Message, state: FSMContext):
    await message.answer("Введите название новой категории:")
    await state.set_state(AddCategory.waiting_for_category_name)

@dp.message(AddCategory.waiting_for_category_name)
async def receive_category_name(message: types.Message, state: FSMContext):
    category_name = message.text
    await add_category(category_name)
    await message.answer(f"Категория '{category_name}' успешно добавлена.")
    await state.clear()  # Очистка состояния

@dp.message(Command('addexpense'))
async def add_expense_handler(message: types.Message, state: FSMContext):
    await message.answer("Введите дату расхода (в формате ГГГГ-ММ-ДД):")
    await state.set_state(AddExpense.waiting_for_date)

@dp.message(AddExpense.waiting_for_date)
async def receive_expense_date(message: types.Message, state: FSMContext):
    try:
        date = datetime.strptime(message.text, "%Y-%m-%d")
        await state.update_data(expense_date=date)
        await message.answer("Введите сумму расхода:")
        await state.set_state(AddExpense.waiting_for_price)
    except ValueError:
        await message.answer("Некорректный формат даты. Пожалуйста, введите дату в формате ГГГГ-ММ-ДД.")

@dp.message(AddExpense.waiting_for_price)
async def receive_expense_price(message: types.Message, state: FSMContext):
    try:
        price = float(message.text)
        await state.update_data(expense_price=price)
        await message.answer("Введите категорию расхода:")
        await state.set_state(AddExpense.waiting_for_category)
    except ValueError:
        await message.answer("Некорректный формат суммы. Пожалуйста, введите число.")

@dp.message(AddExpense.waiting_for_category)
async def receive_expense_category(message: types.Message, state: FSMContext):
    category_name = message.text
    data = await state.get_data()
    date = data['expense_date']
    price = data['expense_price']
    #TODO необходимо добавить пользователя по ключу
    user_id = message.chat.id

    await add_expense(user_id, date, price, category_name)
    await message.answer(f"Расход на сумму {price} в категории '{category_name}' за {date} успешно добавлен.")
    await state.clear()


# серверное событие
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
