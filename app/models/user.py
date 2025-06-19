from sqlalchemy import Column, Integer, String
from app.db.database import Base


class User(Base):
    """
    Модель пользователя системы.

    Атрибуты:
    - username: уникальное имя пользователя
    - email: уникальный email
    - hashed_password: хешированный пароль
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
