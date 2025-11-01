from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# --- FIX 1: database MUST be imported pehle to define 'Base' ---
from database import engine, get_db, Base # Base is included for completeness
import models, schemas #
# --- FIX END ---

# This line ensures the 'tasks' table is created in the database file
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TO-DO-LIST Pure Backend API",
    description="Full CRUD API using FastAPI, Pydantic, and SQLAlchemy.",
)

# --- CRUD ENDPOINTS ---

# 1. CREATE (POST)
@app.post("/tasks/", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Creates a new To-Do task in the database."""
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# 2. READ ALL (GET)
@app.get("/tasks/", response_model=List[schemas.TaskResponse])
def read_all_tasks(db: Session = Depends(get_db)):
    """Retrieves all tasks."""
    return db.query(models.Task).all()

# 3. READ ONE (GET)
@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """Retrieves a single task by its ID."""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task Not Found. Check the ID parameter.")
    return db_task

# 4. UPDATE (PATCH)
@app.patch("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task_data: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """Updates one or more fields of an existing task."""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task Not Found.")

    # Get only the fields provided in the request body
    update_data = task_data.model_dump(exclude_unset=True)
    
    # Update the DB model instance
    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task

# 5. DELETE (DELETE)
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Deletes a task by its ID."""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task Not Found.")

    db.delete(db_task)
    db.commit()
    return