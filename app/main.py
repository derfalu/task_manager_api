from fastapi import FastAPI
from app.api import user, task, tag
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(tag.router)
app.include_router(task.router)
