from main import get_friends
from config import USER_ID

def test_get_friends():
    out = get_friends(USER_ID)
    assert 'friendslist' in out
    assert 'friends' in out['friendslist']
    assert len(out['friendslist']['friends']) == 22