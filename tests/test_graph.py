from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

@pytest.fixture
def sample_graph_payload():
    return {
        "nodes": [{"name": "A"}, {"name": "B"}, {"name": "C"}],
        "edges": [{"source": "A", "target": "B"}, {"source": "B", "target": "C"}]
    }

def test_create_graph_success(sample_graph_payload):
    response = client.post("/api/graph/", json=sample_graph_payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert isinstance(data["id"], int)

def test_create_graph_cycle_error():
    # Создаем граф с циклом: A -> B -> A
    cyclic_payload = {
        "nodes": [{"name": "A"}, {"name": "B"}],
        "edges": [{"source": "A", "target": "B"}, {"source": "B", "target": "A"}]
    }
    response = client.post("/api/graph/", json=cyclic_payload)
    assert response.status_code == 400
    assert "Graph contains a cycle" in response.text

def test_read_graph_not_found():
    response = client.get("/api/graph/99999/")
    assert response.status_code == 404
    assert "Graph entity not found" in response.text

def test_delete_node_not_found():
    response = client.delete("/api/graph/99999/node/NonexistentNode")
    assert response.status_code == 404

def test_full_graph_flow(sample_graph_payload):
    # Создаем граф
    create_resp = client.post("/api/graph/", json=sample_graph_payload)
    graph_id = create_resp.json()["id"]

    # Читаем граф
    read_resp = client.get(f"/api/graph/{graph_id}/")
    assert read_resp.status_code == 200
    read_data = read_resp.json()
    assert read_data["id"] == graph_id
    assert len(read_data["nodes"]) == 3
    assert len(read_data["edges"]) == 2

    # Получаем список смежности
    adj_resp = client.get(f"/api/graph/{graph_id}/adjacency_list")
    assert adj_resp.status_code == 200
    adj = adj_resp.json()
    assert isinstance(adj, dict)
    assert set(adj.keys()) == {"A", "B", "C"}

    # Получаем обратный список смежности
    rev_adj_resp = client.get(f"/api/graph/{graph_id}/reverse_adjacency_list")
    assert rev_adj_resp.status_code == 200
    rev_adj = rev_adj_resp.json()
    assert isinstance(rev_adj, dict)
    assert set(rev_adj.keys()) == {"A", "B", "C"}

    # Удаляем вершину "B"
    del_resp = client.delete(f"/api/graph/{graph_id}/node/B")
    assert del_resp.status_code == 204

    # Читаем граф после удаления
    read_after_del_resp = client.get(f"/api/graph/{graph_id}/")
    read_after_del = read_after_del_resp.json()
    node_names = [node["name"] for node in read_after_del["nodes"]]
    assert "B" not in node_names
