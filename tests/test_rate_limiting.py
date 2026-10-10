import pytest
from unittest.mock import patch
from app.routes import app, limiter
from app.graph import graphs

# The /graph route calls get_friends() directly, so it must be mocked here.
# A private profile makes the route return early, with no further Steam calls.
PRIVATE_PROFILE = {"is_private": True, "friends": []}
REQUEST = {"id": "76561197999528143", "session_id": "test-session"}


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


@patch("app.routes.get_friends", return_value=PRIVATE_PROFILE)
def test_friends_within_limit(mock_get_friends, client):
    response = client.post("/graph", json=REQUEST)
    assert response.status_code == 200


@patch("app.routes.get_friends", return_value=PRIVATE_PROFILE)
def test_friends_exceeds_limit(mock_get_friends, client):
    for i in range(10):
        client.post("/graph", json=REQUEST)

    response = client.post("/graph", json=REQUEST)
    assert response.status_code == 429
