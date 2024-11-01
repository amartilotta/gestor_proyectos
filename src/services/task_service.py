from fastapi import logger
from schemas.task_schema import TaskCreateSchema, TaskUpdateSchema
from sqlmodel import Session, select

from api.errors.task_error import TaskNotFoundError
from models.task_model import Task


class TaskService:
    @staticmethod
    async def create_task(task: TaskCreateSchema, session: Session):
        db_task = Task.model_validate(task)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
    async def updated_task(id: int, task: TaskUpdateSchema, session: Session):

        db_task = session.get(Task, id)
        if not db_task:
            logger.error("TODO")
            raise TaskNotFoundError()
        update_data = task.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)

        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
    async def get_task(session: Session):
        tasks = session.exec(select(Task)).all()
        task_dumped = [task.model_dump() for task in tasks]
        return task_dumped

    @staticmethod
    async def get_task_by_id(id: int, session: Session):
        task = session.get(Task, id)
        return task

    @staticmethod
    async def delete_task_by_id(id: int, session: Session):
        task = session.get(Task, id)
        if not task:
            raise TaskNotFoundError()
        session.delete(task)
        session.commit()
        return task
