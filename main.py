import requests
import re
from urllib.error import HTTPError
from config import STEAM_API_KEY, USER_ID

def get_friends(user_id):
    """Returns a user's Steam friends"""

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