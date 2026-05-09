from unittest.mock import patch
from app.services import lookup_ids

STEVE_ID = "76561197999528143"
STEVE = {"steamid": STEVE_ID, "personaname": "Steve"}

JIM_ID = "76561198047699484"
JIM = {"steamid": JIM_ID, "personaname": "Jim"}

@patch("app.cache.player_cache.get")
@patch("app.cache.player_cache.set")
@patch("app.services.requests.get")
def test_all_misses(mock_requests_get, mock_cache_set, mock_cache_get):
    mock_cache_get.return_value = None
    mock_requests_get.return_value.json.return_value = {
        "response": {"players": [STEVE, JIM]}
    }

    result = lookup_ids([STEVE_ID, JIM_ID])

    assert result == {STEVE_ID: STEVE, JIM_ID: JIM}
    mock_requests_get.assert_called_once()

@patch("app.cache.player_cache.get")
@patch("app.services.requests.get")
def test_all_hits(mock_requests_get, mock_cache_get):
    mock_cache_get.side_effect = lambda id: {STEVE_ID: STEVE, JIM_ID: JIM}[id]

    result = lookup_ids([STEVE_ID, JIM_ID])

    assert result == {STEVE_ID: STEVE, JIM_ID: JIM}
    mock_requests_get.assert_not_called()

@patch("app.cache.player_cache.get")
@patch("app.cache.player_cache.set")
@patch("app.services.requests.get")
def test_partial_hits(mock_requests_get, mock_cache_set, mock_cache_get):
    mock_cache_get.side_effect = lambda id: STEVE if id == STEVE_ID else None

    mock_requests_get.return_value.json.return_value = {
        "response": {"players": [JIM]}
    }

    result = lookup_ids([STEVE_ID, JIM_ID])

    assert result == {STEVE_ID: STEVE, JIM_ID: JIM}
    url = mock_requests_get.call_args[0][0]
    assert JIM_ID in url
    assert STEVE_ID not in url
