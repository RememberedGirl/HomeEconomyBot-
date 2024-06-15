import os
from sqlalchemy.ext.asyncio import create_async_engine

from config import DATABASE_NAME
from db.models import Base


# Формируем URL для подключения к базе данных
DATABASE_URL = f"sqlite+aiosqlite:///{os.path.join(os.path.dirname(__file__), DATABASE_NAME)}"

# Создаем асинхронный движок базы данных
engine = create_async_engine(DATABASE_URL, echo=True)


# Функция для создания таблиц в базе данных
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Инициализация базы данных
if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
