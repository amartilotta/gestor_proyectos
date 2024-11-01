from fastapi import Depends
from fastapi.responses import JSONResponse
from schemas.task_schema import TaskCreateSchema, TaskUpdateSchema
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

    @staticmethod
    async def updated_task(
        id: int,
        task: TaskUpdateSchema,
        session: Session = Depends(get_session),
    ):
        db_updated_task = await TaskService.updated_task(id, task, session)

        return JSONResponse(
            {"message": "Task updated", "task": db_updated_task.model_dump()},
            status_code=200,
        )

    @staticmethod
    async def get_task(session: Session = Depends(get_session)):
        db_tasks = await TaskService.get_task(session)
        return JSONResponse(
            {"message": "Succefull", "tasks": db_tasks},
            status_code=200,
        )

    @staticmethod
    async def get_task_by_id(id: int, session: Session = Depends(get_session)):
        db_task = await TaskService.get_task_by_id(id, session)
        return JSONResponse(
            {"message": "Succefull", "task": db_task.model_dump()},
            status_code=200,
        )

    @staticmethod
    async def delete_task_by_id(
        id: int, session: Session = Depends(get_session)
    ):
        db_task = await TaskService.delete_task_by_id(id, session)
        return JSONResponse(
            {
                "message": "Task deleted successfully",
                "task": db_task.model_dump(),
            },
            status_code=200,
        )
