from typing import List, Optional
from pydantic import BaseModel

class WorkflowBase(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str] = None


class WorkflowCreate(BaseModel):
    name: str
    description: Optional[str] = None


class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class NodeBase(BaseModel):
    type: str
    name: str
    description: Optional[str] = None

class NodeCreate(NodeBase):
    pass

class EdgeBase(BaseModel):
    source_node_id: int
    target_node_id: int

class EdgeCreate(EdgeBase):
    pass
