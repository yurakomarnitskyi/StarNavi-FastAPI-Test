"""
Schemas that validate Workflow model.
"""
from typing import Optional
from pydantic import BaseModel

class WorkflowBase(BaseModel):
    """Base workflow schema return all fields"""
    id: Optional[int]
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


class WorkflowCreate(BaseModel):
    """Schema for creating workflow."""
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


class WorkflowUpdate(BaseModel):
    """Schema for update workflow."""
    name: Optional[str] = None
    description: Optional[str] = None


