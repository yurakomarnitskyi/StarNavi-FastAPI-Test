"""
Edge api endpoints.
"""
from sqlalchemy.orm import Session
from fastapi import (
    HTTPException,
    Depends,
    APIRouter
)
from database.database import SessionLocal
from edge import schemas
from database import models


router = APIRouter()


def get_db():
    """Fucntion uses to connect with database"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/workflow/{workflow_id}/edges", response_model=schemas.EdgeCreate)
def create_edge(source_node_id: int, target_node_id: int, workflow_id: int, db: Session = Depends(get_db)):
    """Create edge method user can input three argument"""
    existing_workflow = db.query(models.Workflow).filter(models.Workflow.id == workflow_id).first()
    if not existing_workflow:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )

    new_edge = models.Edge(source_node_id=source_node_id, target_node_id=target_node_id)
    db.add(new_edge)
    db.commit()
    db.refresh(new_edge)

    return new_edge
