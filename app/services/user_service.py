from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import pwd_context


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_user(db: Session, user: UserCreate):
    if (
        db.query(User)
        .filter((User.username == user.username) | (User.email == user.email))
        .first()
    ):
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким именем или email уже существует",
        )
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
