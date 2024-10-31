from fastapi import Depends
from fastapi.responses import JSONResponse
from schemas.task_schema import TaskCreateSchema
from sqlmodel import Session

from database.connection import get_session
from services.task_service import TaskService


class TaskController:
    @staticmethod
    async def create_task(
        task: TaskCreateSchema, session: Session = Depends(get_session)
    ):
        db_task = await TaskService.create_task(task, session)

        return JSONResponse(
            {"message": "Task created", "task": db_task.model_dump()},
            status_code=201,
        )
