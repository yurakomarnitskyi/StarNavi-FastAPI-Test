import sys
import os

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_dir)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_workflow():
    data = {     
        "name": "My workflow",
        "description": "English"
    }
    response = client.post('/workflows/', json=data)  # Виправлено URL та використано метод json для передачі даних
    assert response.status_code == 200

