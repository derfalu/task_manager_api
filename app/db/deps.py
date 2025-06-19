from app.db.database import SessionLocal
from sqlalchemy.orm import Session


def get_db() -> Session:
    """
    Зависимость для получения сессии базы данных в маршрутах и сервисах.

    Создаёт локальную сессию через SessionLocal,
    автоматически закрывает соединение после завершения запроса.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
