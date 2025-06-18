from sqlalchemy.orm import Session
from app.models.tag import Tag
from app.schemas.tag import TagCreate
from app.models.user import User
from typing import List
from fastapi import HTTPException


def get_all_tags(db: Session, user: User):
    return db.query(Tag).filter(Tag.user_id == user.id).all()


def get_or_create_tags(db: Session, tag_names: List[str], user: User) -> List[Tag]:
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
    existing = (
        db.query(Tag).filter(Tag.name == tag_in.name, Tag.user_id == user.id).first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Тег с таким именем уже существует")
    tag = Tag(name=tag_in.name, user_id=user.id)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


def delete_tag(db: Session, tag_id: int, user: User):
    tag = db.query(Tag).filter(Tag.id == tag_id, Tag.user_id == user.id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Тег не найден")
    if tag.tasks:
        raise HTTPException(
            status_code=400, detail="Нельзя удалить тег, связанный с задачами"
        )
    db.delete(tag)
    db.commit()
