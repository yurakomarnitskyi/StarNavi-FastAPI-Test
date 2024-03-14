"""
Node api endpoints.
"""
from fastapi import (
    HTTPException,
    Depends,
    status,
    Response)
from sqlalchemy.orm import Session
from node.crud import NodeCrudOperations
from node import schemas
from database.database import SessionLocal
from fastapi import APIRouter
from database import models
from workflow.crud import WorkflowCrudOperations


crud_workflow = WorkflowCrudOperations()


crud_node = NodeCrudOperations()


router = APIRouter()


def get_db():
    """Fucntion use to connect with database"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/workflow/{workflow_id}/start_node", response_model=schemas.NodeCreate)
def start_workflow(name: str, description: str, workflow_id: int, db: Session = Depends(get_db)):
    """Start node endpoint."""
    existing_workflow = db.query(models.Workflow).filter(models.Workflow.id == workflow_id).first()

    if not existing_workflow:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )

    start_node = crud_node.process_start_node(db=db, workflow_id=workflow_id, 
                                              name=name, description=description)

    if start_node:
        return start_node
    else:
        raise HTTPException(status_code=400, detail="Unable to create start node.")


@router.post("/workflows/{workflow_id}/nodes/message/", response_model=schemas.MessageNodeCreate)
def create_message_node(workflow_id: int, name: str, description: str, text: str, 
                        status: str, db: Session = Depends(get_db)):
    """Message node endpoint."""
    workflow = crud_workflow.get_workflow(db, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    message_node = crud_node.create_message_node(db=db, name=name, description=description,
                                                 workflow_id=workflow_id, status=status, text=text)

    return message_node


@router.post("/workflows/{workflow_id}/nodes/condition/", response_model=schemas.ConditionNodeCreate)
def create_condition_node(workflow_id: int, db: Session = Depends(get_db)):
    """Condition endpoint."""
    condition_node = crud_node.process_condition_node(db, workflow_id)
    if condition_node:
        return condition_node
    else:
        raise HTTPException(status_code=400, detail="Unable to create condition node")


@router.post("/workflow/{workflow_id}/nodes/end/", response_model=schemas.EndNodeCreate)
def create_end_node(workflow_id: int, name: str, description: str, db: Session = Depends(get_db)):
    """End node endpoint."""
    end_node = crud_node.create_end_node(db=db, workflow_id=workflow_id, 
                                         name=name, description=description)
    if end_node:
        return end_node
    else:
        raise HTTPException(status_code=400, detail="Unable to create end node")


@router.get('/node/{node_id}/', response_model=schemas.NodeBase)
def get_node(node_id: int, db: Session = Depends(get_db)):
    """Endpoint to get node obcjet with id."""
    db_node = crud_node.get_node(db, node_id)
    if db_node:
        return db_node
    else:
        return HTTPException(status_code=404, detail='Node not found')


@router.patch('/nodes/{node_id}', response_model=schemas.NodeBase)
def update_node(node_id: int, update_node: schemas.NodeUpdate, db: Session = Depends(get_db)):
    """Endpoint to update node object with id."""
    db_node = crud_node.update_node(db, node_id, update_node)

    if db_node is None:
        return HTTPException(status_code=404, detail="Node not found")
    return db_node


@router.delete('/nodes/{node_id}', response_model=schemas.NodeBase)
def delete_node(node_id: int, db: Session = Depends(get_db)):
    """Endpoint to delete node object with id."""
    db_node = crud_node.get_node(db, node_id)

    if db_node is None:
        return HTTPException(status_code=404, detail="Node not found")

    crud_node.delete_node(db, node_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/workflows/{workflow_id}/run/", response_model=schemas.WorkflowPath)
def run_workflow(workflow_id: int, db: Session = Depends(get_db)):
    """Endpint that show all path."""
    try:
        workflow_path = crud_node.run_workflow(db=db, workflow_id=workflow_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ve))
    return workflow_path

