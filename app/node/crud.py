from sqlalchemy.orm import Session
from database import models, schemas
from fastapi import HTTPException, status


def create_node(db: Session, node: schemas.NodeCreate):
  
    db_workflow = db.query(models.Workflow).filter(models.Workflow.id == node.workflow_id).first()
    if not db_workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow with id {node.workflow_id} not found",
        )

    db_node = models.Node(**node.dict())
    db.add(db_node)
    db.commit()
    db.refresh(db_node)
    return db_node


def get_node(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Node).offset(skip).limit(limit).all()


def update_node(db: Session, node_id: int, updated_node: schemas.WorkflowUpdate):
    db_node= db.query(models.Workflow).filter(models.Node.id == node_id).first()

    if db_node:
        for key, value in updated_node.dict().items():
            setattr(db_node, key, value)

        db.commit()
        db.refresh(db_node)

    return db_node


def delete_node(db: Session, node_id: int):
    db_node = db.query(models.Node).filter(models.Node.id == node_id).first()

    if db_node:
        db.delete(db_node)
        db.commit()

    return db_node
