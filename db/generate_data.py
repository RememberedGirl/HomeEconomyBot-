import random
from datetime import datetime, timedelta

from db.database import AsyncSessionLocal
from db.models import User, Expense, Category
from sqlalchemy.future import select



# Функция для генерации случайной даты в диапазоне от start до end
def random_date(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))


# Функция для генерации тестовых данных
async def generate_data():
    async with AsyncSessionLocal as session:
        # Генерация пользователей
        users = ["user1", "user2", "user3"]
        for username in users:
            user = User(username=username)
            session.add(user)

        # Генерация расходов
        categories = ["food", "transport", "entertainment", "utilities"]
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 12, 31)
        for _ in range(20):  # Генерируем 20 расходов
            user_id = random.randint(1, len(users))  # Выбираем случайного пользователя
            date = random_date(start_date, end_date)  # Генерируем случайную дату
            price = round(random.uniform(10, 100), 2)  # Генерируем случайную цену
            category_name = random.choice(categories)  # Выбираем случайную категорию

            # Получаем объект категории по ее имени
            category = await session.execute(select(Category).filter(Category.name == category_name))
            category = category.scalar_one_or_none()

            if category is None:
                category = Category(name=category_name)
                session.add(category)
                await session.flush()

            # Создаем объект расхода с указанием категории
            expense = Expense(user_id=user_id, date=date, price=price, category_id=category.id)
            session.add(expense)

        await session.commit()


# Запуск генерации данных
if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(generate_data())
