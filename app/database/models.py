"""
Database models for all app.
"""
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, relationship
from enum import Enum as PythonEnum



DATABASE_URL = "sqlite:///./test.db"


engine = create_engine(DATABASE_URL)
Base = declarative_base()


class NodeType(str, PythonEnum):
    """NodeType model that connect with node model and using with schemas."""
    start = "start"
    message = "message"
    condition = "condition"
    end = "end"


class NodeStatus(str, PythonEnum):
    """NodeStatus model that connect with node model and using with schemas."""
    pending = "pending"
    sent = "sent"
    opened = "opened"


class Workflow(Base):
    """Workflow model configuration."""
    __tablename__ = "workflows"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)


class Node(Base):
    """Node model configurattion."""
    __tablename__ = "nodes"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(NodeType), index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    text = Column(String, nullable=True)
    status = Column(Enum(NodeStatus), default=None, nullable=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"))
    workflow = relationship("Workflow", back_populates="nodes")
    incoming_edges = relationship("Edge", back_populates="target_node", foreign_keys="Edge.target_node_id")
    outgoing_edges = relationship("Edge", back_populates="source_node", foreign_keys="Edge.source_node_id")


class Edge(Base):
    """Edge model configuration."""
    __tablename__ = "edges"
    id = Column(Integer, primary_key=True, index=True)
    source_node_id = Column(Integer, ForeignKey("nodes.id"))
    target_node_id = Column(Integer, ForeignKey("nodes.id"))
    source_node = relationship("Node", back_populates="outgoing_edges", foreign_keys=[source_node_id])
    target_node = relationship("Node", back_populates="incoming_edges", foreign_keys=[target_node_id])


Workflow.nodes = relationship("Node", back_populates="workflow")
Base.metadata.create_all(bind=engine)
