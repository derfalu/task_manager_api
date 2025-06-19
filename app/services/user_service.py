from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import pwd_context
from app.core.exceptions import existing_user_exception


def get_password_hash(password: str):
    """
    Хеширует пароль с использованием bcrypt.

    :param password: Обычный текстовый пароль
    :return: Хешированный пароль
    """
    return pwd_context.hash(password)


def create_user(db: Session, user: UserCreate):
    """
    Создаёт нового пользователя, если имя и email уникальны.

    :param db: Сессия SQLAlchemy
    :param user: Данные нового пользователя
    :raises: existing_user_exception, если пользователь с таким именем или email уже есть
    :return: Объект созданного пользователя
    """
    existing_user = (
        db.query(User)
        .filter((User.username == user.username) | (User.email == user.email))
        .first()
    )

    if existing_user:
        raise existing_user_exception()

    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_password(plain_password, hashed_password):
    """
    Проверяет соответствие введённого пароля хешу.

    :param plain_password: Введённый пароль
    :param hashed_password: Хеш, сохранённый в БД
    :return: True, если пароль верный
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_username(db: Session, username: str):
    """
    Получает пользователя по имени.

    :param db: Сессия SQLAlchemy
    :param username: Имя пользователя
    :return: Объект пользователя или None
    """
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, username: str, password: str):
    """
    Аутентифицирует пользователя по имени и паролю.

    :param db: Сессия SQLAlchemy
    :param username: Имя пользователя
    :param password: Пароль
    :return: Объект пользователя при успехе, иначе None
    """
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
