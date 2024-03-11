from sqlalchemy.orm import Session
from database import models, schemas
from fastapi import HTTPException, status

def create_edge(db: Session, edge: schemas.EdgeCreate):
    db_node_sourse = db.query(models.Node).filter(models.Node.id == edge.source_node_id).first()
    db_node_target = db.query(models.Node).filter(models.Node.id == edge.target_node_id).first()
    if not db_node_sourse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Node with source {edge.source_node_id} not found."
        )
    if not db_node_target:
        raise HTTPException(
              status_code=status.HTTP_404_NOT_FOUND,
              detail=f"Node with target ID {edge.target_node_id} not found."
        )

    db_edge = models.Edge(**edge.dict())
    db.add(db_edge)
    db.commit()
    db.refresh(db_edge)
    return db_edge

