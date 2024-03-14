"""
Schemas that validate Node model.
"""
from typing import List, Optional
from pydantic import BaseModel
from database.models import NodeStatus, NodeType


class NodeBase(BaseModel):
    """Node base"""
    id: Optional[int]
    type: NodeType
    name: str
    text: Optional[str] = None 
    status: Optional[NodeStatus] = None  
    description: str
    workflow_id: Optional[int] = None


class NodeCreate(NodeBase):
    """Schema for creating Node and inherits NodeBase."""
    pass


class NodeUpdate(BaseModel):
    """Schema for updating Node."""
    type: NodeType
    name: str
    text: str
    description: str
    status: NodeStatus = None
    workflow_id: Optional[int] = None


class NodeRead(BaseModel):
    """Schema for get node with id."""
    id: int


class NodeDelete(BaseModel):
    """Shema for delete node with id."""
    id: int


class MessageNodeCreate(BaseModel):
    """Schema for creating message node."""
    id: int
    type: NodeType
    name: str
    description: str
    text: str
    status: NodeStatus = None


class ConditionNodeCreate(BaseModel):
    """Schema for condition node."""
    id: int
    type: NodeType
    name: str
    description: str
    workflow_id: Optional[int] = None


class EndNodeCreate(BaseModel):
    """Schema for end node."""
    id: int
    type: NodeType
    name: str
    description: str
    workflow_id: Optional[int] = None


class WorkflowNode(BaseModel):
    """Schema uses to retrun obcjets field."""
    id: int
    type: Optional[NodeType] = None
    name: str
    description: Optional[str] = ""
    text: Optional[str] = ""
    status: Optional[NodeStatus] = None
    workflow_id: Optional[int] = None


class WorkflowPath(BaseModel):
    """Schema uses to return path and inherits WorkflowNode."""
    path: List[WorkflowNode]
