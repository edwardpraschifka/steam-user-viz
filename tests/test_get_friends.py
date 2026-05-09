from unittest.mock import patch
import requests
import pytest
import os
from app.services import get_friends
from app.config import USER_ID

@patch("app.cache.friends_cache.get", return_value=None)
@patch("app.cache.friends_cache.set")
@patch("app.services.requests.get")
def test_miss(mock_requests_get, mock_cache_set, mock_cache_get):

    mock_requests_get.return_value.json.return_value = {
    "friendslist": {
        "friends": [
            {
                "steamid": "76561197999528143",
                "relationship": "friend",
                "friend_since": 1499051558
            },
            {
                "steamid": "76561198047699484",
                "relationship": "friend",
                "friend_since": 1453093050
            }
        ]
    }
    }

    result = get_friends(USER_ID)

    mock_requests_get.assert_called_once()

    assert result == {
        "is_private": False,
        "friends": [
            {
                "steamid": "76561197999528143",
                "relationship": "friend",
                "friend_since": 1499051558
            },
            {
                "steamid": "76561198047699484",
                "relationship": "friend",
                "friend_since": 1453093050
            }
        ]
    }

@patch("app.cache.friends_cache.get", return_value=None)
@patch("app.cache.friends_cache.set")
@patch("app.services.requests.get")
def test_private(mock_requests_get, mock_cache_set, mock_cache_get):

    mock_requests_get.return_value.status_code = 401

    result = get_friends(USER_ID)

    assert result == {"is_private": True, "friends": []}

@patch("app.cache.friends_cache.get", return_value=None)
@patch("app.cache.friends_cache.set")
@patch("app.services.requests.get")
def test_no_friends(mock_requests_get, mock_cache_set, mock_cache_get):

    mock_requests_get.return_value.json.return_value = {
    "friendslist": {
        "friends": []
    }
    }

    result = get_friends(USER_ID)

    assert result == {"is_private": False, "friends": []}

def test_invalid_user():
    with pytest.raises(ValueError):
        get_friends("invalid user id")

@patch("app.cache.friends_cache.get", return_value=None)
@patch("app.cache.friends_cache.set")
@patch("app.services.requests.get")
def test_timeout(mock_requests_get, mock_cache_set, mock_cache_get):
    mock_requests_get.side_effect = requests.exceptions.Timeout

    with pytest.raises(RuntimeError):
        get_friends(USER_ID)

@patch("app.cache.friends_cache.get")
@patch("app.services.requests.get")
def test_hit(mock_requests_get, mock_cache_get):
    mock_cache_get.side_effect = lambda id: {
        "is_private": False,
        "friends": [
            {
                "steamid": "76561197999528143",
                "relationship": "friend",
                "friend_since": 1499051558
            },
            {
                "steamid": "76561198047699484",
                "relationship": "friend",
                "friend_since": 1453093050
            }
        ]
    }

    result = get_friends(USER_ID)

    assert result == {
        "is_private": False, 
        "friends": [
            {
                "steamid": "76561197999528143",
                "relationship": "friend",
                "friend_since": 1499051558
            },
            {
                "steamid": "76561198047699484",
                "relationship": "friend",
                "friend_since": 1453093050
            }
        ]
    }
    mock_requests_get.assert_not_called()