from fastapi import FastAPI
from workflow import workflow_router

app = FastAPI()

app.include_router(
    workflow_router.router,
)
