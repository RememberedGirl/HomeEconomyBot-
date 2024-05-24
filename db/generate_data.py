import random
from datetime import datetime, timedelta
from database import add_user, add_expense

# Функция для генерации случайной даты в диапазоне от start до end
def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))

# Функция для генерации тестовых данных
async def generate_data():
    # Генерация пользователей
    users = ["user1", "user2", "user3"]
    for username in users:
        await add_user(username)

    # Генерация расходов
    categories = ["food", "transport", "entertainment", "utilities"]
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    for _ in range(20):  # Генерируем 20 расходов
        user_id = random.randint(1, len(users))  # Выбираем случайного пользователя
        date = random_date(start_date, end_date)  # Генерируем случайную дату
        price = round(random.uniform(10, 100), 2)  # Генерируем случайную цену
        category = random.choice(categories)  # Выбираем случайную категорию
        await add_expense(user_id, date, price, category)

# Запуск генерации данных
if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(generate_data())
