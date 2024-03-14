"""
Crud operations with workflow.
"""
from sqlalchemy.orm import Session
from database import models
from workflow import schemas



def create_workflow(db: Session, workflow: schemas.WorkflowCreate):
    """Create workflow method."""
    db_workflow = models.Workflow(**workflow.dict())
    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)
    return db_workflow


def get_workflow(db: Session, workflow_id: int):
    """Get workflow method with id ."""
    return db.query(models.Workflow).filter(models.Workflow.id == workflow_id).first()


def get_workflows(db: Session, skip: int = 0, limit: int = 10):
    """Get all workflow objects."""
    return db.query(models.Workflow).offset(skip).limit(limit).all()


def update_workflow(db: Session, workflow_id: int, updated_workflow: schemas.WorkflowUpdate):
    """Update workflow method."""
    db_workflow = db.query(models.Workflow).filter(models.Workflow.id == workflow_id).first()

    if db_workflow:
        for key, value in updated_workflow.dict().items():
            setattr(db_workflow, key, value)

        db.commit()
        db.refresh(db_workflow)

    return db_workflow


def delete_workflow(db: Session, workflow_id: int):
    """Delete workflow method with id"""
    db_workflow = db.query(models.Workflow).filter(models.Workflow.id == workflow_id).first()

    if db_workflow:
        db.delete(db_workflow)
        db.commit()

    return db_workflow
