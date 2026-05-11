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


@patch("app.routes.get_friends", return_value=[])
@patch("app.routes.lookup_ids", return_value={})
def test_friends_within_limit(mock_lookup, mock_friends, client):
    response = client.get("/friends?user_id=76561197999528143")
    assert response.status_code == 200


@patch("app.routes.get_friends", return_value=[])
@patch("app.routes.lookup_ids", return_value={})
def test_friends_exceeds_limit(mock_lookup, mock_friends, client):
    for i in range(10):
        client.get("/friends?user_id=76561197999528143")
    
    response = client.get("/friends?user_id=76561197999528143")
    assert response.status_code == 429

