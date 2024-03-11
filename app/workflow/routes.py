from fastapi import (
    HTTPException,
    Depends,
    status,
    Response)
from sqlalchemy.orm import Session
import workflow.crud as crud_workflow
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


@router.post('/workflows/', response_model=schemas.WorkflowBase)
def create_workflow(workflow: schemas.WorkflowCreate, db: Session = Depends(get_db)):
    return crud_workflow.create_workflow(db, workflow)


@router.get('/workflow/{workflow_id}', response_model=schemas.WorkflowBase)
def get_workflow(workflow_id: int, db: Session = Depends(get_db)):
    db_workflow = crud_workflow.get_workflow(db, workflow_id)
    if db_workflow is None:
        return HTTPException(status_code=404, detail='Workflow not found')
    return db_workflow


@router.get('/workflows/', response_model=List[schemas.WorkflowBase])
def read_workflows(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
     workflows = crud_workflow.get_workflows(db, skip=skip, limit=limit)
     return workflows


@router.put('/workflows/{workflow_id}', response_model=schemas.WorkflowBase)
def update_workflow(workflow_id: int, updated_workflow: schemas.WorkflowUpdate, db: Session = Depends(get_db)):
    db_workflow = crud_workflow.update_workflow(db, workflow_id, updated_workflow)
        
    if not db_workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
        
    return db_workflow


@router.patch('/workflows/{workflow_id}', response_model=schemas.WorkflowBase)
def patch_workflow(workflow_id: int, updated_workflow: schemas.WorkflowUpdate, db: Session = Depends(get_db)):
    db_workflow = crud_workflow.update_workflow(db, workflow_id, updated_workflow)
      
    if not db_workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
       
    return db_workflow


@router.delete('/workflows/{workflow_id}', response_model=schemas.WorkflowBase)
def delete_workflow(workflow_id: int, db: Session = Depends(get_db)):
    db_workflow = crud_workflow.get_workflow(db, workflow_id)

    if db_workflow is None:
        return HTTPException(status_code=404, detail="Workflow not found")

    crud_workflow.delete_workflow(db, workflow_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
