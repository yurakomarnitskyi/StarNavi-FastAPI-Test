"""
Test with node endpint.
"""
import sys
import os
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_dir)


from fastapi.testclient import TestClient
import pytest
from app.main import app
from node.crud import delete_all_node


client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_database():
    """Delete all data from database after each test."""
    yield
    delete_all_node()


data_workflow = {
    "name": "Test workflow",
    "description": "Test",
}


def test_node_start():
    """Test for creating node."""
    response_workflow = client.post('/workflows/', json=data_workflow)
    workflow_id = response_workflow.json()["id"]

    response_node = client.post(f'/workflow/{workflow_id}/start_node?name=ded&description=hjk')
    assert response_node.status_code == 200
    assert response_node.json()['type'] == 'start'


def test_message_node():
    """Test for creating message node."""
    response_workflow = client.post('/workflows/', json=data_workflow)
    workflow_id = response_workflow.json()["id"]

    response_node = client.post(
        f'/workflows/{workflow_id} \
        /nodes/message/?name=Test&description=About%20something%20&text=Hello&status=opened')

    assert response_node.status_code == 200
    assert response_node.json()['type'] == 'message'
    assert response_node.json()['status'] == 'opened'


def test_condition_node():
    """Test for creating condition node."""
    response_workflow = client.post('/workflows/', json=data_workflow)
    workflow_id = response_workflow.json()["id"]

    client.post(
        f'/workflows/{workflow_id} \
        /nodes/message/?name=Test&description=About%20something%20&text=Hello&status=opened')

    response_node = client.post(f'/workflows/{workflow_id}/nodes/condition/')

    assert response_node.status_code == 200
    assert response_node.json()['description'] == 'Condition Node with No edge'


def test_end_node():
    """Test for creating end node."""
    response_workflow = client.post('/workflows/', json=data_workflow)
    workflow_id = response_workflow.json()["id"]

    response_node = client.post(f'/workflow/{workflow_id}/nodes/end/?name=Endnode&description=Test')
    assert response_node.status_code == 200
    assert response_node.json()['type'] == 'end'
    assert response_node.json()['description'] == 'Test'


def test_get_node():
    """Test get node for id."""
    response_workflow = client.post('/workflows/', json=data_workflow)
    workflow_id = response_workflow.json()["id"]

    client.post(f'/workflow/{workflow_id}/nodes/end/?name=End%20node%20&description=Test')
    client.post(f'/workflow/{workflow_id}/start_node?name=ded&description=hjk')

    response = client.get('/node/1')

    assert response.status_code == 200
    assert response.json()['name'] == 'End node '
    assert response.json()['description'] != 'ded'


def test_update_node():
    """Test for update node."""
    response_workflow = client.post('/workflows/', json=data_workflow)
    workflow_id = response_workflow.json()["id"]

    client.post(f'/workflow/{workflow_id}/nodes/end/?name=End%20node%20&description=Test')

    update_data = {
        "type": "start",
        "name": "update ndoe",
        "text": "string",
        "description": "new",
        "status": "pending",
        "workflow_id": 1
    }

    response = client.patch('/nodes/1', json=update_data)

    assert response.status_code == 200


def test_delete_node():
    """Test for delete method."""
    response_workflow = client.post('/workflows/', json=data_workflow)
    workflow_id = response_workflow.json()["id"]

    client.post(f'/workflow/{workflow_id}/nodes/end/?name=End%20node%20&description=Test')

    response = client.delete('/nodes/1')
    assert response.status_code == 204


def test_create_edge():
    """Test for creating edge with node."""
    response_workflow = client.post('/workflows/', json=data_workflow)
    workflow_id = response_workflow.json()["id"]

    client.post(f'/workflow/{workflow_id}/start_node?name=ded&description=hjk')
    client.post(
        f'/workflows/{workflow_id} \
        /nodes/message/?name=Test&description=About%20something%20&text=Hello&status=opened')

    response = client.post('workflow/1/edges?source_node_id=1&target_node_id=2')
    assert response.status_code == 200
    assert response.json()['source_node_id'] == 1
    assert response.json()['target_node_id'] == 2


def test_return_path():
    """Test for return all path star and end."""
    response_workflow = client.post('/workflows/', json=data_workflow)
    workflow_id = response_workflow.json()["id"]

    client.post(f'/workflow/{workflow_id}/start_node?name=ded&description=hjk')
    client.post(
        f'/workflows/{workflow_id} \
        /nodes/message/?name=Test&description=About%20something%20&text=Hello&status=opened')
    client.post(f'/workflows/{workflow_id}/nodes/condition/')
    client.post(f'/workflow/{workflow_id}/nodes/end/?name=Endnode&description=Test')

    client.post('workflow/1/edges?source_node_id=1&target_node_id=2')
    client.post('workflow/1/edges?source_node_id=2&target_node_id=3')
    client.post('workflow/1/edges?source_node_id=3&target_node_id=4')

    response = client.post(f'/workflows/{workflow_id}/run/')
    assert response.status_code == 200
    assert len(response.json()['path']) == 4

