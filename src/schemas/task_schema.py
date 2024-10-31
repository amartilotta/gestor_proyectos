from typing import List, Optional

from pydantic import BaseModel


class TaskCreateSchema(BaseModel):
    title: str
    description: str


class TaskUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: bool = False


class TaskResponse(TaskCreateSchema):
    id: int
    completed: bool = False


class TaskOutput(BaseModel):
    message: str
    task: TaskResponse


class TaskGetOutput(BaseModel):
    message: str
    tasks: List[TaskResponse]
