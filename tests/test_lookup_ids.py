from unittest.mock import patch
import requests
import pytest
import os
from app.services import lookup_ids

@patch("app.services.requests.get")
def test_lookup_ids(mock_get):

    mock_get.return_value.json.return_value = {
        "response": {
            "players": [
                {
                    "steamid": "76561197999528143",
                    "personaname": "Steve"
                },
                {
                    "steamid": "76561198047699484",
                    "personaname": "Jim"
                }
            ]
        }
    }

    result = lookup_ids(["76561197999528143", "76561198047699484"])

    assert result == {
        "76561197999528143": {
                "steamid": "76561197999528143",
                "personaname": "Steve"
        },
        "76561198047699484": {
                "steamid": "76561198047699484",
                "personaname": "Jim"
        }
    }

