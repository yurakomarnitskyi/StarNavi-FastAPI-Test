"""
Schemas that validate Edge model.
"""
from pydantic import BaseModel


class EdgeBase(BaseModel):
    """Uses with return Edge objects."""
    source_node_id: int
    target_node_id: int
    
    class Config:
        orm_mode = True


class EdgeCreate(EdgeBase):
    """Uses with crating Edge and inherits EdgeBase"""
    pass
