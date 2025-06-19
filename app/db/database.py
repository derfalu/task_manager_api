from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core import settings

# URL подключения к базе данных, формируется через настройки приложения
DATABASE_URL = settings.driver_database_url

# Создание движка SQLAlchemy
engine = create_engine(DATABASE_URL)

# Создание фабрики сессий для работы с БД
SessionLocal = sessionmaker(
    autocommit=False,  # Требует явного вызова commit()
    autoflush=False,  # Отключает автоматический flush перед запросами
    bind=engine,  # Привязываем к текущему движку
)

# Базовый класс для всех моделей SQLAlchemy
Base = declarative_base()
