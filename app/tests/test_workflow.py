"""
Test with workflow endpint.
"""
import sys
import os
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_dir)


from fastapi.testclient import TestClient
import pytest
from app.main import app
from workflow.crud import delete_all_workflows


client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_database():
    """Delete all data from database after each test."""
    yield
    delete_all_workflows()


def test_create_workflow():
    """Tets with post method."""
    data = {     
        "name": "My workflow",
        "description": "English"
    }
    response = client.post('/workflows/', json=data)
    assert response.status_code == 200
    assert response.json()['name'] == data["name"]


def test_get_workflow():
    """Test with get method."""
    data = {
        "name": "Another workflow",
        "description": "Another description"
    }
    client.post('/workflows/', json=data)

    response = client.get('/workflows/')
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_workflow_all():
    """Test for update workflow."""
    data = {
        "name": "Another workflow",
        "description": "Another description"
    }
    client.post('/workflows/', json=data)

    update_data = {
        "name": "Update name",
        "description": 'Update',
    }
    response = client.put('/workflows/1/', json=update_data)

    assert response.status_code == 200
    assert response.json()['name'] == update_data['name']


def test_update_workflow_name():
    """Test for update workflow name."""
    data = {
        "name": "Update name",
        "description": 'Update',
    }

    client.post('/workflows/', json=data)

    update_data = {
        "name": "new_name",
    }
    response = client.patch('/workflows/1/', json=update_data)

    assert response.status_code == 200
    assert response.json()['name'] == 'new_name'


def test_delete_workflow():
    """Test delete workflow use id."""
    data = {
        "name": "Update name",
        "description": 'Update',
    }

    client.post('/workflows/', json=data)

    response = client.delete('/workflows/1/')

    assert response.status_code == 204
