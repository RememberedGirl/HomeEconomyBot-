from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

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

