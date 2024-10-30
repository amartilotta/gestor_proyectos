from fastapi import APIRouter, HTTPException
from app.schemas.task_schema import TaskCreate, TaskOutput
from app.models.task_model import Task

router = APIRouter()
tasks_db = []  # Temporal "base de datos" en memoria

@router.post("/tasks/", response_model=TaskOutput, status_code=201)
async def create_task(task: TaskCreate):
    new_task = Task(id=len(tasks_db) + 1, **task.model_dump())
    tasks_db.append(new_task)
    return {"message": "Task created", "task": new_task}