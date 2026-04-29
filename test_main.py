from unittest.mock import patch
import requests
import pytest
import os
from main import get_friends
from config import USER_ID

@patch("main.requests.get")
def test_normal(mock_get):

    mock_get.return_value.json.return_value = {
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

@patch("main.requests.get")
def test_private(mock_get):

    mock_get.return_value.status_code = 401

    result = get_friends(USER_ID)

    assert result == {"is_private": True, "friends": []}

@patch("main.requests.get")
def test_no_friends(mock_get):

    mock_get.return_value.json.return_value = {
    "friendslist": {
        "friends": []
    }
    }

    result = get_friends(USER_ID)

    assert result == {"is_private": False, "friends": []}

def test_invalid_user():                                                
    with pytest.raises(ValueError):
        get_friends("invalid user id")

@patch("main.requests.get")                                                   
def test_bad_api_key(mock_get):
    mock_get.return_value.ok = True                                           
    mock_get.return_value.status_code = 400
    mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("400")
                                                                            
    with pytest.raises(RuntimeError):
        get_friends(USER_ID)

@patch("main.requests.get")
def test_timeout(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout                        

    with pytest.raises(RuntimeError):                                         
        get_friends(USER_ID)