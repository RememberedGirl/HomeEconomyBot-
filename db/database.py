from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from create_db import engine, AsyncSessionLocal

# Базовый класс для определения моделей данных
Base = declarative_base()

# Определяем модель данных для таблицы пользователей
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)

# Определяем модель данных для таблицы расходов
class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    price = Column(Float)
    category = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="expenses")

# Определяем связь между пользователем и его расходами
User.expenses = relationship("Expense", back_populates="user")

# Функция для добавления нового пользователя
async def add_user(username):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            user = User(username=username)
            session.add(user)

# Функция для получения списка всех пользователей
async def get_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        return result.scalars().all()

# Функция для добавления нового расхода
async def add_expense(user_id, date, price, category):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            expense = Expense(user_id=user_id, date=date, price=price, category=category)
            session.add(expense)
