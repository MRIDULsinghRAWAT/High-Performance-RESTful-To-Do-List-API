from pydantic import BaseModel
from typing import Optional

# 1. Base structure 
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

# 2. Input for creating a task
class TaskCreate(TaskBase):
    pass

# 3. Input for updating a task
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

# 4. Output/Response model
class TaskResponse(TaskBase):
    id: int
    is_completed: bool

    class Config:
        from_attributes = True