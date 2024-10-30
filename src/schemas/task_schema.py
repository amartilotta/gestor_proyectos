from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str


class TaskResponse(TaskCreate):
    id: int
    completed: bool = False

    class Config:
        orm_mode = True


class TaskOutput(BaseModel):
    message: str
    task: TaskResponse
