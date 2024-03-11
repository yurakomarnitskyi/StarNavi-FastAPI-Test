from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, Session, relationship
from enum import Enum as PythonEnum
from sqlalchemy.sql import text


DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
Base = declarative_base()


class NodeType(str, PythonEnum):
    start = "start"
    message = "message"
    condition = "condition"
    end = "end"


class NodeStatus(str, PythonEnum):
    pending = "pending"
    sent = "sent"
    opened = "opened"

class Workflow(Base):
    __tablename__ = "workflows"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    nodes = relationship("Node", back_populates="workflow")


class Node(Base):
    __tablename__ = "nodes"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(NodeType), index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(Enum(NodeStatus), default=None, nullable=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"))
    workflow = relationship("Workflow", back_populates="nodes")
    incoming_edges = relationship("Edge", back_populates="target_node", foreign_keys="Edge.target_node_id")
    outgoing_edges = relationship("Edge", back_populates="source_node", foreign_keys="Edge.source_node_id")


class Edge(Base):
    __tablename__ = "edges"
    id = Column(Integer, primary_key=True, index=True)
    source_node_id = Column(Integer, ForeignKey("nodes.id"))
    target_node_id = Column(Integer, ForeignKey("nodes.id"))
    source_node = relationship("Node", back_populates="outgoing_edges", foreign_keys=[source_node_id])
    target_node = relationship("Node", back_populates="incoming_edges", foreign_keys=[target_node_id])


Workflow.nodes = relationship("Node", back_populates="workflow")
Base.metadata.create_all(bind=engine)
