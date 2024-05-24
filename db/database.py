import os
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select

from config import DATABASE_NAME
# Изменим импорт моделей на новый путь
from db.models import User, Expense, Category, Base

# Изменим путь для создания URL базы данных
DATABASE_URL = f"sqlite+aiosqlite:///{os.path.join(os.path.dirname(__file__), DATABASE_NAME)}"

# Создаем асинхронный движок AsyncEngine для работы с базой данных
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем объект AsyncSessionLocal для работы с базой данных
AsyncSessionLocal = AsyncSession(bind=engine)

# Функция для добавления нового пользователя
async def add_user(username):
    async with AsyncSessionLocal as session:
        async with session.begin():
            user = User(username=username)
            session.add(user)

# Функция для получения пользователя по chat_id
async def get_user(chat_id):
    async with AsyncSessionLocal as session:
        result = await session.execute(select(User).filter_by(username=chat_id))
        return result.scalar_one_or_none()

# Функция для получения списка всех пользователей
async def get_users():
    async with AsyncSessionLocal as session:
        result = await session.execute(select(User))
        return result.scalars().all()

# Функция для добавления нового расхода
async def add_expense(user_id, date, price, category_name):
    async with AsyncSessionLocal as session:
        async with session.begin():
            # Получаем объект категории из базы данных по имени категории
            category = await session.execute(select(Category).filter(Category.name == category_name))
            category = category.scalar_one_or_none()

            # Если категория не найдена, добавляем новую категорию в базу данных
            if category is None:
                category = Category(name=category_name)
                session.add(category)
                await session.flush()  # Вызываем flush, чтобы получить значение ID новой категории

            # Создаем объект расхода с указанием категории
            expense = Expense(user_id=user_id, date=date, price=price, category=category)
            session.add(expense)

# Функция для добавления новой категории
async def add_category(name):
    async with AsyncSessionLocal as session:
        async with session.begin():
            category = Category(name=name)
            session.add(category)


