from aiogram import types
from db import add_expense, get_expenses

async def handle_start(message: types.Message):
    await message.reply("Привет! Я бот для учета семейных расходов.")

async def handle_help(message: types.Message):
    await message.reply("Список доступных команд:\n/start - Начать работу\n/help - Получить помощь\n/add_expense - Добавить расход\n/view_expenses - Просмотреть расходы")

async def handle_add_expense(message: types.Message):
    try:
        _, amount, category = message.text.split(maxsplit=2)
        amount = float(amount)
        await add_expense(amount, category)
        await message.reply(f"Добавлен расход: {amount} на {category}.")
    except ValueError:
        await message.reply("Неверный формат команды. Используйте: /add_expense <сумма> <категория>")

async def handle_view_expenses(message: types.Message):
    expenses = await get_expenses()
    if expenses:
        response = "Список расходов:\n"
        for amount, category, date in expenses:
            response += f"{amount} на {category} (Дата: {date})\n"
    else:
        response = "Нет данных о расходах."
    await message.reply(response)
