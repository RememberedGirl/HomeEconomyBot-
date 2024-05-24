import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base

# Путь к файлу базы данных
DATABASE_NAME = 'family_bot.db'

# Формируем URL для подключения к базе данных
DATABASE_URL = f"sqlite+aiosqlite:///{os.path.join(os.path.dirname(__file__), DATABASE_NAME)}"

# Создаем асинхронный движок базы данных
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем сессию для работы с базой данных
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Функция для создания таблиц в базе данных
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Инициализация базы данных
if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
