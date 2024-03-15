"""
Crud operations with Node.
"""
from sqlalchemy.orm import Session
from database import models
from node import schemas
from database.models import Node, NodeStatus, NodeType, Edge
import networkx as nx
from fastapi import HTTPException
from database.database import SessionLocal


def delete_all_node():
    """Clean database method."""
    db = SessionLocal()
    try:
        db.query(Node).delete()
        db.commit()
    finally:
        db.close()


class NodeCrudOperations:
    """Class with node endpoint."""


    def get_node(self, db: Session, node_id: int):
        """Get node object with its associated workflow."""
        return db.query(models.Node).filter(models.Node.id == node_id).first()


    def update_node(self, db: Session, node_id: int, updated_node: schemas.NodeUpdate):
        """Update method with nodes"""

        db_node = db.query(models.Node).join(
            models.Workflow, models.Workflow.id == models.Node.workflow_id).filter(
                models.Node.id == node_id).first()

        if not db_node:
            raise HTTPException(status_code=404, detail='Node id not found')

        if updated_node.workflow_id == 0:
            raise HTTPException(status_code=404, detail='Workflow id not found')

        if updated_node.workflow_id:
            workflow_id = db.query(models.Workflow).filter(
                models.Workflow.id == updated_node.workflow_id).first()
            if not workflow_id:
                raise HTTPException(status_code=404, detail='Workflow id not found')

        for key, value in updated_node.dict().items():
            setattr(db_node, key, value)

        db.commit()
        db.refresh(db_node)

        return db_node


    def delete_node(self, db: Session, node_id: int):
        """Delete method."""
        db_node = db.query(models.Node).filter(models.Node.id == node_id).first()

        if db_node:
            db.delete(db_node)
            db.commit()

        return db_node


    def process_start_node(self, db: Session, name: str, description: str, workflow_id: int):
        """Method with creating node."""
        start_node = Node(type=NodeType.start, name=name, description=description, workflow_id=workflow_id)
        db.add(start_node)
        db.commit()
        db.refresh(start_node)
        return start_node


    def create_message_node(self, db: Session, name: str, description: str, workflow_id: int, 
                            text: str, status: str):
        """Creating message node method."""
        message_node = models.Node(type=models.NodeType.message, text=text,
                                    name=name, description=description, status=status, 
                                    workflow_id=workflow_id)
        db.add(message_node)
        db.commit()
        db.refresh(message_node)
        return message_node


    def process_condition_node(self, db: Session, workflow_id: int):
        """Condition node method."""
        prev_node = db.query(Node).filter(
            Node.workflow_id == workflow_id).order_by(Node.id.desc()).first()

        if prev_node and prev_node.type == NodeType.message and prev_node.status == NodeStatus.sent:
            message_node = Node(type=NodeType.message, name="Message node (Yes)",
                                description="Messsage with Yes edge", workflow_id=workflow_id)
            
            db.add(message_node)
            db.commit()
            db.refresh(message_node)

            edge = Edge(source_node=prev_node, target_node=message_node)
            db.add(edge)
            db.commit()

            return message_node

        else:
            condition_node = Node(type=NodeType.condition, name="Condition Node (No)",
                                description="Condition Node with No edge", workflow_id=workflow_id)
            db.add(condition_node)
            db.commit()
            db.refresh(condition_node)

            edge = Edge(source_node=prev_node, target_node=condition_node)
            db.add(edge)
            db.commit()

            return condition_node


    def create_end_node(self, db: Session, name: str, description: str, workflow_id: int):
        """End node method."""
        end_node = Node(type=NodeType.end, name=name, description=description, workflow_id=workflow_id)
        db.add(end_node)
        db.commit()
        db.refresh(end_node)
        return end_node


    def run_workflow(self, db: Session, workflow_id: int) -> schemas.WorkflowPath:
        """Run workflow mwrhod show all path."""
        nodes = db.query(models.Node).filter(models.Node.workflow_id == workflow_id).all()

        G = nx.DiGraph()

        for node in nodes:
            G.add_node(node.id)

        for node in nodes:
            for edge in node.outgoing_edges:
                G.add_edge(edge.source_node_id, edge.target_node_id)

        start_node = next((node for node in nodes if node.type == schemas.NodeType.start), None)

        if not start_node:
            raise ValueError("Start node not found in the workflow.")

        end_node = next((node for node in nodes if node.type == schemas.NodeType.end), None)

        if not end_node:
            raise ValueError("End node not found in the workflow.")

        try:
            path_ids = nx.shortest_path(G, source=start_node.id, target=end_node.id)
            path_nodes = []
            for node_id in path_ids:

                node = db.get(models.Node, node_id)

                path_node = schemas.WorkflowNode(
                    id=node.id,
                    type=node.type,
                    name=node.name,
                    description=node.description,
                    text=node.text,
                    status=node.status,
                    workflow_id=node.workflow_id
                )
                path_nodes.append(path_node)

        except nx.NetworkXNoPath:
            raise ValueError("Could not reach end node from start node.")

        return schemas.WorkflowPath(path=path_nodes)
