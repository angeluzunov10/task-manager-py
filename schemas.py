from pydantic import BaseModel
from typing import Optional

# Базова схема със споделени полета
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None # description е опционално поле, може да е празно

# Схема за създаване на задача с допълнителни полета
class TaskCreate(TaskBase):
    task_type: str # поле за типа на задачата (WorkTask или PersonalTask)
    deadline: Optional[str] = None # само за WorkTask
    priority: Optional[str] = None # само за PersonalTask

# Схема за отговор при извличане на задача (това, което API връща)
class TaskResponse(TaskBase):
    id: int
    status: str
    type: str

    class Config:
        from_attributes = True # позволява на Pydantic да създава обекти чрез SQLAlchemy модели


