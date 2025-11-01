from sqlalchemy import Column, Integer, String, Boolean
# Corrected Import: Must use absolute path
from database import Base 

class Task(Base):
    """
    SQLAlchemy Model for the 'tasks' table.
    """
    # --- FIX 2: Must use double underscore (__) ---
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)