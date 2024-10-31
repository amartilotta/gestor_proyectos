
from controller.task_controller import TaskController
from fastapi import APIRouter, Depends, HTTPException
from schemas.task_schema import (
    TaskGetOutput,
    TaskOutput,
    TaskUpdateSchema,
)
from sqlmodel import Session, select

from database.connection import get_session
from models.task_model import Task
from tools.custom_logger import Logger

router = APIRouter()

logger = Logger("app_log", "app_folder", severity="info")


#router.post("/tasks/", TaskController.create_task)

router.add_api_route("/tasks/", TaskController.create_task, methods=["POST"])


@router.put("/tasks/{id}")
async def put(
    id: int, task: TaskUpdateSchema, session: Session = Depends(get_session)
):
    db_task = session.get(Task, id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = task.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return {"message": "Task updated", "task": db_task}


@router.get("/tasks/", response_model=TaskGetOutput, status_code=200)
async def get_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    return {"message": "Tasks", "tasks": tasks}


@router.get("/tasks/{id}", response_model=TaskOutput, status_code=200)
async def get_task_by_id(id: int, session: Session = Depends(get_session)):
    task = session.get(Task, id)
    return {"message": "Task", "task": task}


@router.delete("/tasks/{id}", response_model=TaskOutput, status_code=200)
async def delete_task_by_id(id: int, session: Session = Depends(get_session)):
    task = session.get(Task, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully", "task": task}


# @router.put("/tasks/{id}", response_model=dict, status_code=200)
# async def update_task(
#     id: int, task: TaskCreateSchema, session: Session = Depends(get_session)
# ):
#     db_task = session.get(Task, id)
#     logger.info("-------------1")
#     if not db_task:
#         raise HTTPException(status_code=404, detail="Task not found")

#     update_data = task.model_dump(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(db_task, key, value)

#     logger.info("-------------2")

#     session.add(db_task)
#     session.commit()
#     session.refresh(db_task)

#     return {"message": "Task updated successfully", "task": db_task}
