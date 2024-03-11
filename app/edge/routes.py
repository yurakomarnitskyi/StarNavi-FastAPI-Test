from sqlalchemy.orm import Session
import edge.crud as crud_edge
from fastapi import (
    HTTPException,
    Depends,
    status,
    Response,
    APIRouter
)
from database.database import SessionLocal, engine
from database import schemas


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/edge/', response_model=schemas.EdgeBase)
def create_edge(edges: schemas.EdgeCreate, db: Session = Depends(get_db)):
    return crud_edge.create_edge(db, edges)
