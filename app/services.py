import requests
import re
import time
from urllib.error import HTTPError

from concurrent.futures import ThreadPoolExecutor, as_completed

from .config import STEAM_API_KEY, USER_ID
from .cache import friends_cache, player_cache
from . import metrics

def validate_id(user_id: str):
    """Checks if ID exists and is valid"""

    if not user_id:
        raise ValueError("Missing Steam ID")
    
    if not re.fullmatch(r'\d{17}', str(user_id)):                                      
      raise ValueError(f"Invalid Steam ID: {user_id}")
    
def get_with_backoff(url: str, timeout=10, max_retries=3):
    """Make request to URL with exponential backoff"""
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout)
            metrics.api_call_count = metrics.api_call_count + 1
            metrics.last_api_call = {"time": time.time(), "success": response.ok}
            if response.ok:
                return response
            if attempt == max_retries - 1:
                response.raise_for_status()
        except requests.exceptions.Timeout:
            if attempt == max_retries - 1:
                raise
        time.sleep(2 ** attempt)

def get_friends(id: str):
    """Get list of user's friends"""

    result = {}

    # raise error if id is invalid
    validate_id(id)

    # return cache entry for id,
    # if it exists
    cache_entry = friends_cache.get(id)
    if cache_entry is not None:
        return cache_entry

    url = (
        "https://api.steampowered.com/"
        "ISteamUser/GetFriendList/v0001/"
        f"?key={STEAM_API_KEY}"
        f"&steamid={id}"
        "&relationship=friend"
    )

    try:
        response = get_with_backoff(url)

        # private user
        if response.status_code == 401:
            result = {"is_private": True, "friends": []}
        elif not response.ok:
            response.raise_for_status()
        else:
            data = response.json()
            friends = data.get("friendslist", {}).get("friends", [])
            result = {"is_private": False, "friends": friends}

        if not result["is_private"]:
            friends_cache.set(id, result)
        return result
    
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Steam API request failed: {e}")
    
def lookup_ids(ids: list):
    """
    Takes a list of Steam IDs and
    returns a dictionary mapping each ID to the
    corresponding profile.
    """

    result = {}
    misses = []

    for id in ids:
        validate_id(id)
        cache_entry = player_cache.get(id)
        if cache_entry is not None:
            result[id] = cache_entry
        else:
            misses.append(id)

    if misses:
        url = (
            "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
            f"?key={STEAM_API_KEY}"
            f"&steamids={','.join(misses)}"
        )

        try:
            response = get_with_backoff(url)
            response.raise_for_status()
            data = response.json()
            players = data.get("response", {}).get("players", [])
            for player in players:
                player_cache.set(player["steamid"], player)
                result[player["steamid"]] = player

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Steam API request failed: {e}")

    return result

def lookup_ids_bulk(ids: list, batch_size=100, max_workers=5):
      """Split id list into sublists and calls lookup_ids on each"""
      
      batches = [ids[i:i+batch_size] for i in range(0, len(ids), batch_size)]
      result = {}
      with ThreadPoolExecutor(max_workers=max_workers) as executor:
          futures = {executor.submit(lookup_ids, batch): batch for batch in batches}
          for future in as_completed(futures):
              result.update(future.result())
      return result

def get_recently_played(id: str):
    """Fetches stats on the user's recently played games"""

    result = {}

    url = (
            "https://api.steampowered.com/IPlayerService/"
            f"GetRecentlyPlayedGames/v0001/?key={STEAM_API_KEY}"
            f"&steamid={id}&format=json"
    )

    try:
        response = get_with_backoff(url)
        response.raise_for_status()
        data = response.json()
        games = data.get("response", {})
        result = games
        
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Steam API request failed: {e}")
    
    return result

def get_owned_games(id: str):
    """Fetches stats on the user's owned games"""
    
    result = {}

    url = (
            "https://api.steampowered.com/IPlayerService/"
            f"GetOwnedGames/v0001/?key={STEAM_API_KEY}"
            f"&steamid={id}&format=json&include_appinfo=true"
    )

    try:
        response = get_with_backoff(url)
        response.raise_for_status()
        data = response.json()
        games = data.get("response", {})
        result = games
        
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Steam API request failed: {e}")
    
    return result