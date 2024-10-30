from fastapi import FastAPI
from app.api import tasks_router

app = FastAPI()

app.include_router(tasks_router.router)