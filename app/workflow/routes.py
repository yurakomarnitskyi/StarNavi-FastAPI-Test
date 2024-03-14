"""
Workflow api endpoints.
"""
from fastapi import (
    HTTPException,
    Depends,
    status,
    Response)
from sqlalchemy.orm import Session
import workflow.crud as crud_workflow
from workflow import schemas
from database.database import SessionLocal
from typing import List
from fastapi import APIRouter


router = APIRouter()


def get_db():
    """Fucntion use to connect with database"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/workflows/', response_model=schemas.WorkflowBase)
def create_workflow(workflow: schemas.WorkflowCreate, db: Session = Depends(get_db)):
    """Endpoint with creating workflow."""
    return crud_workflow.create_workflow(db, workflow)


@router.get('/workflow/{workflow_id}', response_model=schemas.WorkflowBase)
def get_workflow(workflow_id: int, db: Session = Depends(get_db)):
    """Endpoint to get workflow object with id."""
    db_workflow = crud_workflow.get_workflow(db, workflow_id)
    if db_workflow is None:
        return HTTPException(status_code=404, detail='Workflow not found')
    return db_workflow


@router.get('/workflows/', response_model=List[schemas.WorkflowBase])
def read_workflows(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Endpoint to get all workflow objcets."""
    workflows = crud_workflow.get_workflows(db, skip=skip, limit=limit)
    return workflows


@router.put('/workflows/{workflow_id}', response_model=schemas.WorkflowBase)
def update_workflow(workflow_id: int, updated_workflow: schemas.WorkflowUpdate,
                     db: Session = Depends(get_db)):
    """Endpoint use put method to update workflow with id."""
    db_workflow = crud_workflow.update_workflow(db, workflow_id, updated_workflow)
        
    if not db_workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
        
    return db_workflow


@router.patch('/workflows/{workflow_id}', response_model=schemas.WorkflowBase)
def patch_workflow(workflow_id: int, updated_workflow: schemas.WorkflowUpdate,
                    db: Session = Depends(get_db)):
    """Endpoint use patch method to update workflow with id."""
    db_workflow = crud_workflow.update_workflow(db, workflow_id, updated_workflow)

    if not db_workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return db_workflow


@router.delete('/workflows/{workflow_id}', response_model=schemas.WorkflowBase)
def delete_workflow(workflow_id: int, db: Session = Depends(get_db)):
    """Endpoint to delete workflow with id."""
    db_workflow = crud_workflow.get_workflow(db, workflow_id)

    if db_workflow is None:
        return HTTPException(status_code=404, detail="Workflow not found")

    crud_workflow.delete_workflow(db, workflow_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
