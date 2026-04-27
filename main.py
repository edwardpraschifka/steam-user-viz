import requests
from config import STEAM_API_KEY

def get_friends(user_id):
    """For a given user id, return a list of the user's friends"""

    url = f"https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={STEAM_API_KEY}&steamid={user_id}&relationship=friend"
    r = requests.get(url)

    if r.ok:
        # current format is {'friendslist': {'friends': [friend_1, friend_2, ...]}}
        # extract [friend_1, friend_2, ...]
        friends = r.json()['friendslist']['friends']

        # each friend has format {steam_id, relationship, friend_since}
        # extract steam_ids as a list
        ids = {friend["steamid"] for friend in friends}
        return ids
    else:
        raise RuntimeError(f"Error: {url} responded with code {r.status_code}")