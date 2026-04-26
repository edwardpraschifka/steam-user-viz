from main import get_friends
from config import USER_ID

def test_get_friends():
    out = get_friends(USER_ID)
    assert type(out) == list
    assert "steamid" in out[0].keys() 
    assert "relationship" in out[0].keys()
    assert "friend_since" in out[0].keys()