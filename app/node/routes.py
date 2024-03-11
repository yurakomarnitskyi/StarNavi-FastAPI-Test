from fastapi import (
    HTTPException,
    Depends,
    status,
    Response)
from sqlalchemy.orm import Session
import node.crud as crud_node
import database.schemas as schemas
from database.database import SessionLocal, engine
from typing import List
from fastapi import APIRouter


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/nodes/', response_model=schemas.NodeBase)
def create_nodes(nodes: schemas.NodeCreate, db: Session = Depends(get_db)):
    return crud_node.create_node(db, nodes)


@router.get('/nodes/', response_model=List[schemas.NodeBase])
def read_node(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
     nodes = crud_node.get_node(db, skip=skip, limit=limit)
     return nodes

@router.patch('/nodes/{node_id}', response_model=schemas.NodeBase)
def update_node(node_id: int, update_node: schemas.NodeUpdate, db: Session = Depends(get_db)):
    db_node = crud_node.update_node(db, node_id, update_node)

    if db_node is None:
        return HTTPException(status_code=404, detail="Node not found")
    return db_node


@router.delete('/nodes/{node_id}', response_model=schemas.NodeBase)
def delete_node(node_id: int, db: Session = Depends(get_db)):
    db_node = crud_node.get_node(db, node_id)

    if db_node is None:
        return HTTPException(status_code=404, detail="Node not found")
   
    crud_node.delete_node(db, node_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
