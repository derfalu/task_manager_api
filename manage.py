import os
from alembic.config import Config
from alembic import command
from app.db.database import Base, engine
import uvicorn


def drop_all():
    print("🧨 Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Tables dropped.")

def generate_migration():
    print("📄 Generating new Alembic migration...")
    alembic_cfg = Config("alembic.ini")
    command.revision(alembic_cfg, message="autogenerate", autogenerate=True)
    print("✅ Migration generated.")


def run_migrations():
    print("📦 Running Alembic migrations...")
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    print("✅ Migrations applied.")


def run_server():
    print("🚀 Starting FastAPI server...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    drop_all()
    generate_migration()
    run_migrations()
    run_server()
