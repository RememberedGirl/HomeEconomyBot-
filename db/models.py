from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Модель данных для таблицы пользователей
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    expenses = relationship("Expense", back_populates="user")

# Модель данных для таблицы расходов
class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey('categories.id'))  # Внешний ключ для связи с таблицей категорий
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")

# Модель данных для таблицы категорий расходов
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    expenses = relationship("Expense", back_populates="category")

# Связываем категории с расходами
Category.expenses = relationship("Expense", back_populates="category")
