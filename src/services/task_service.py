from schemas.task_schema import TaskCreateSchema
from sqlmodel import Session

from models.task_model import Task


class TaskService:
    @staticmethod
    async def create_task(task: TaskCreateSchema, session: Session):
        db_task = Task.model_validate(task)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task
