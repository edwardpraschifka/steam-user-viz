import pytest
import json
from unittest.mock import patch
import app.metrics as metrics
from app.routes import app


@pytest.fixture(autouse=True)
def reset_metrics():
    metrics.api_call_count = 0
    metrics.last_api_call = {}
    yield


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_health_response_structure(client):
    response = client.get("/health")
    data = json.loads(response.data)
    assert "time" in data
    assert "api_call_count" in data
    assert "cache_hit_rate" in data
    assert "friends_cache" in data["cache_hit_rate"]
    assert "player_cache" in data["cache_hit_rate"]
    assert "last_api_call" in data


def test_health_zero_counts(client):
    response = client.get("/health")
    data = json.loads(response.data)
    assert data["api_call_count"] == 0
    assert data["cache_hit_rate"]["friends_cache"] == "0%"
    assert data["cache_hit_rate"]["player_cache"] == "0%"
    assert data["last_api_call"] == {}


def test_health_api_call_count(client):
    metrics.api_call_count = 3
    response = client.get("/health")
    data = json.loads(response.data)
    assert data["api_call_count"] == 3


def test_health_last_api_call(client):
    metrics.last_api_call = {"time": 1000.0, "success": True}
    response = client.get("/health")
    data = json.loads(response.data)
    assert data["last_api_call"] == {"time": 1000.0, "success": True}


def test_health_cache_hit_rate(client):
    from app.cache import friends_cache, player_cache
    with patch.object(friends_cache, "hit_count", 3), \
         patch.object(friends_cache, "miss_count", 1), \
         patch.object(player_cache, "hit_count", 1), \
         patch.object(player_cache, "miss_count", 1):
        response = client.get("/health")
        data = json.loads(response.data)
        assert data["cache_hit_rate"]["friends_cache"] == "75.0%"
        assert data["cache_hit_rate"]["player_cache"] == "50.0%"
