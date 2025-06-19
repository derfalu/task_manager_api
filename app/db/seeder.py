import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.db.database import SessionLocal
from app.models.user import User
from app.models.task import Task
from app.models.tag import Tag
from sqlalchemy.exc import IntegrityError
from app.services.user_service import get_password_hash


def seed_users(db):
    print("🔹 Сеем пользователей...")
    if not db.query(User).first():
        hash_pass_1 = get_password_hash("admin_password")
        hash_pass_2 = get_password_hash("demo_password")
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=hash_pass_1, 
        )
        demo = User(
            username="demo",
            email="demo@example.com",
            hashed_password=hash_pass_2,
        )
        db.add_all([admin, demo])
        db.commit()
        print("✅ Пользователи добавлены.")


def seed_tags(db):
    print("🔹 Сеем теги...")

    user = db.query(User).filter_by(username="admin").first()
    if not user:
        print("❌ Пользователь 'admin' не найден. Пропускаем сидирование тегов.")
        return

    tags = ["urgent", "work", "personal"]

    existing = db.query(Tag).filter(Tag.name.in_(tags), Tag.user_id == user.id).all()
    existing_names = {t.name for t in existing}

    new_tags = [
        Tag(name=name, user_id=user.id) for name in tags if name not in existing_names
    ]

    if new_tags:
        db.add_all(new_tags)
        db.commit()
        print(f"✅ Добавлено тегов: {len(new_tags)}")
    else:
        print("ℹ️ Теги уже существуют.")


def seed_tasks(db):
    print("🔹 Сеем задачи...")

    user = db.query(User).filter_by(username="admin").first()
    if not user:
        print("❌ Пользователь 'admin' не найден. Пропускаем сидирование задач.")
        return

    existing_tasks = db.query(Task).filter(Task.user_id == user.id).first()
    if existing_tasks:
        print("ℹ️ Задачи уже существуют.")
        return

    # Получаем теги
    tags_by_name = {
        tag.name: tag for tag in db.query(Tag).filter(Tag.user_id == user.id).all()
    }

    # Задачи с тегами
    tasks_data = [
        {
            "title": "Сделать проект",
            "description": "Закончить FastAPI проект",
            "tags": ["work", "urgent"],
        },
        {
            "title": "Прочитать статью",
            "description": "Изучить Docker Compose best practices",
            "tags": ["work"],
        },
        {
            "title": "Проверить email",
            "description": "Ответить на важные письма",
            "tags": ["urgent"],
        },
        {
            "title": "Погулять",
            "description": "Пройтись по парку",
            "tags": ["personal"],
        },
        {
            "title": "Купить продукты",
            "description": "Молоко, яйца, хлеб",
            "tags": ["personal", "urgent"],
        },
        {
            "title": "Позвонить маме",
            "description": "Узнать, как дела",
            "tags": ["personal"],
        },
        {
            "title": "Сделать бэкап",
            "description": "Резервное копирование базы данных",
            "tags": ["work"],
        },
        {
            "title": "Обновить зависимости",
            "description": "Запустить pip install -r requirements.txt",
            "tags": ["work"],
        },
        {
            "title": "Записать видео",
            "description": "Обучающее видео по FastAPI",
            "tags": ["work"],
        },
        {
            "title": "Подключить Vue",
            "description": "Интегрировать фронтенд к API",
            "tags": ["work", "urgent"],
        },
        {
            "title": "Устроить уборку",
            "description": "Порядок на рабочем столе и в комнате",
            "tags": ["personal"],
        },
        {
            "title": "Прочитать книгу",
            "description": "Закончить «Чистый код»",
            "tags": ["personal", "work"],
        },
        {
            "title": "Протестировать API",
            "description": "Написать тесты на все endpoints",
            "tags": ["work"],
        },
        {
            "title": "Разобраться с логами",
            "description": "Проанализировать ошибки в docker-compose logs",
            "tags": ["work"],
        },
    ]

    tasks = []
    for data in tasks_data:
        task = Task(
            title=data["title"],
            description=data["description"],
            user_id=user.id,
            tags=[tags_by_name[tag] for tag in data["tags"] if tag in tags_by_name],
        )
        tasks.append(task)

    db.add_all(tasks)
    db.commit()
    print(f"✅ Добавлено задач: {len(tasks)}")


def run():
    print("🚀 Начинаем сидирование...")
    db = SessionLocal()
    try:
        seed_users(db)
        seed_tags(db)
        seed_tasks(db)
    except IntegrityError as e:
        print(f"⚠️ IntegrityError: {e}")
        db.rollback()
    finally:
        db.close()
        print("🏁 Сидирование завершено.")


if __name__ == "__main__":
    run()
