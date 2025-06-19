from sqlalchemy.orm import Session
from app.models.tag import Tag
from app.schemas.tag import TagCreate
from app.models.user import User
from typing import List
from app.core.exceptions import (
    not_found_exception,
    already_exists_exception,
    tag_in_use_exception,
)


def get_all_tags(db: Session, user: User):
    """
    Получает все теги, принадлежащие указанному пользователю.

    :param db: Сессия SQLAlchemy
    :param user: Текущий пользователь
    :return: Список тегов
    """
    return db.query(Tag).filter(Tag.user_id == user.id).all()


def get_or_create_tags(db: Session, tag_names: List[str], user: User) -> List[Tag]:
    """
    Ищет или создаёт теги по названиям. Если тег с заданным именем
    не найден у пользователя, он создаётся. Возвращает список тегов.

    :param db: Сессия SQLAlchemy
    :param tag_names: Список названий тегов
    :param user: Текущий пользователь
    :return: Список объектов Tag
    """
    tags = []
    for name in tag_names:
        tag = db.query(Tag).filter(Tag.name == name, Tag.user_id == user.id).first()
        if not tag:
            tag = Tag(name=name, user_id=user.id)
            db.add(tag)
        tags.append(tag)
    db.flush()
    return tags


def create_tag(db: Session, tag_in: TagCreate, user: User):
    """
    Создаёт новый тег для пользователя. Если тег с таким именем
    уже существует, вызывается исключение already_exists_exception.

    :param db: Сессия SQLAlchemy
    :param tag_in: Данные нового тега
    :param user: Текущий пользователь
    :return: Созданный объект Tag
    """
    existing = (
        db.query(Tag).filter(Tag.name == tag_in.name, Tag.user_id == user.id).first()
    )
    if existing:
        raise already_exists_exception("Тег")
    tag = Tag(name=tag_in.name, user_id=user.id)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


def delete_tag(db: Session, tag_id: int, user: User):
    """
    Удаляет тег по ID, если он принадлежит пользователю.
    Если тег не найден или связан с задачами — выбрасывает исключение.

    :param db: Сессия SQLAlchemy
    :param tag_id: ID удаляемого тега
    :param user: Текущий пользователь
    """
    tag = db.query(Tag).filter(Tag.id == tag_id, Tag.user_id == user.id).first()
    if not tag:
        raise not_found_exception("Тег")
    if tag.tasks:
        raise tag_in_use_exception()
    db.delete(tag)
    db.commit()
