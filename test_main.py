from main import get_friends
from config import USER_ID

def test_get_friends():
    out = get_friends(USER_ID)
    assert type(out) == set