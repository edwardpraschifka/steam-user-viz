import pytest
from unittest.mock import patch
from app.routes import app, limiter
from app.graph import graphs


@pytest.fixture(autouse=True)
def reset_state():
    yield
    limiter.reset()
    graphs.clear()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@patch("app.routes.Graph")
def test_friends_within_limit(mock_graph_class, client):
    mock_graph_class.return_value.serialize.return_value = {}
    response = client.post("/graph", json={"id": "76561197999528143", "session_id": "test-session"})
    assert response.status_code == 200


@patch("app.routes.Graph")
def test_friends_exceeds_limit(mock_graph_class, client):
    mock_graph_class.return_value.serialize.return_value = {}
    for i in range(10):
        client.post("/graph", json={"id": "76561197999528143", "session_id": "test-session"})

    response = client.post("/graph", json={"id": "76561197999528143", "session_id": "test-session"})
    assert response.status_code == 429

