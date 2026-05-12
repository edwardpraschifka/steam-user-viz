import pytest
from unittest.mock import patch
from app.routes import app, limiter


@pytest.fixture(autouse=True)
def reset_limiter():
    yield
    limiter.reset()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@patch("app.routes.graph")
def test_friends_within_limit(mock_graph, client):
    mock_graph.serialize.return_value = {}
    response = client.post("/graph", json={"id": "76561197999528143"})
    assert response.status_code == 200


@patch("app.routes.graph")
def test_friends_exceeds_limit(mock_graph, client):
    mock_graph.serialize.return_value = {}
    for i in range(10):
        client.post("/graph", json={"id": "76561197999528143"})
    
    response = client.post("/graph", json={"id": "76561197999528143"})
    assert response.status_code == 429

