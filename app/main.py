"""
Main file run project and inclide all routes.
"""
from fastapi import FastAPI
from workflow import routes as workflow_routes
from node import routes as node_routes
from edge import routes as edge_routes


app = FastAPI()


app.include_router(workflow_routes.router)
app.include_router(node_routes.router)
app.include_router(edge_routes.router)
