import requests
import re
from urllib.error import HTTPError
from .config import STEAM_API_KEY, USER_ID

def get_friends(user_id):
    """
    Takes a Steam ID and returns a 
    dictionary with the following keys:
    is_private: true if the user's friend list is private, false otherwise
    friends: list of friend Steam IDs (empty if private)
    """

    if not STEAM_API_KEY:
        raise ValueError("Missing Steam API key")
    
    if not re.fullmatch(r'\d{17}', str(user_id)):                                      
      raise ValueError(f"Invalid Steam ID: {user_id}")

    url = (
        "https://api.steampowered.com/"
        "ISteamUser/GetFriendList/v0001/"
        f"?key={STEAM_API_KEY}"
        f"&steamid={user_id}"
        "&relationship=friend"
    )

    try:
        response = requests.get(url, timeout=10)

        # private user
        if response.status_code == 401:
                return {"is_private": True, "friends": []}
        
        response.raise_for_status()

        data = response.json()
        friends = data.get("friendslist", {}).get("friends", [])

        return {"is_private": False, "friends": friends}
    
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Steam API request failed: {e}")
    
def lookup_ids(ids):
    """
    Takes a list of Steam IDs and 
    returns a dictionary mapping each ID to the 
    corresponding player summary.
    """
    
    url = (
        "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
        f"?key={STEAM_API_KEY}"
        f"&steamids={','.join(ids)}"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        players = data.get("response", {}).get("players", [])
        return {player["steamid"]: player for player in players}
    
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Steam API request failed: {e}")