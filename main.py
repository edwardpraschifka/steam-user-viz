import requests
from config import STEAM_API_KEY, USER_ID

def get_friends(user):
    """Returns a Python dictionary of friends for a given user id"""

    url = f"https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={STEAM_API_KEY}&steamid={user}&relationship=friend"
    r = requests.get(url)

    if r.ok:
        return r.json()
    else:
        raise RuntimeError("Error accessing Steam API, check your API key and user ID")
    

out = get_friends(USER_ID)
print(out)
    
