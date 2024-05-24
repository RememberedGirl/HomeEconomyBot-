import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select

from config import DATABASE_NAME
from models import User, Expense, Base

DATABASE_URL = f"sqlite+aiosqlite:///{os.path.join(os.path.dirname(__file__), DATABASE_NAME)}"

# Создаем асинхронный движок AsyncEngine для работы с базой данных
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем объект AsyncSessionLocal для работы с базой данных
AsyncSessionLocal = AsyncSession(bind=engine)

# Функция для создания всех таблиц в базе данных
async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Функция для добавления нового пользователя
async def add_user(username):
    async with AsyncSessionLocal as session:
        async with session.begin():
            user = User(username=username)
            session.add(user)

# Функция для получения списка всех пользователей
async def get_users():
    async with AsyncSessionLocal as session:
        result = await session.execute(select(User))
        return result.scalars().all()

# Функция для добавления нового расхода
async def add_expense(user_id, date, price, category):
    async with AsyncSessionLocal as session:
        async with session.begin():
            expense = Expense(user_id=user_id, date=date, price=price, category=category)
            session.add(expense)

# Вызов каждой функции для проверки
async def test_functions():
    # Создаем все таблицы в базе данных
    await create_all_tables()

    # Добавляем пользователя
    await add_user("test_user")

    # Получаем список всех пользователей
    users = await get_users()
    print("Список пользователей:")
    for user in users:
        print(user.username)

    # Добавляем расход
    await add_expense(1, "2024-05-25", 50.0, "food")
    print("Расход успешно добавлен.")

# Запуск проверки функций
if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_functions())
