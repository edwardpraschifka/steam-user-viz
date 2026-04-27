import requests
import queue
import time
from config import STEAM_API_KEY, USER_ID

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

def bfs(user_id, depth=1, get_friends_func=get_friends):
    """For a given user id and depth, return a dictionary of 
    at most {depth}-degree friends of the user"""

    # dictionary mapping user id's to set of its friends
    id_to_friends = {}

    # queue of user id's to process
    id_queue = queue.Queue()

    # track depth
    friends_in_layer = 1
    friends_processed = 0

    # set containing all enqueued ids
    # (to avoid adding duplicates to queue)
    enqueued = {}

    id_queue.put(user_id)

    while depth > 0:
        id = id_queue.get()
        friends = {}
        

        try:
            friends = get_friends_func(id)
            id_to_friends[id] = friends
        except:
            pass

        for friend_id in friends:
            if friend_id not in id_to_friends and friend_id not in enqueued:
                id_queue.put(friend_id)
                enqueued[friend_id] = True

        friends_processed = friends_processed + 1
        
        if friends_processed == friends_in_layer:
            friends_in_layer = id_queue.qsize()
            depth = depth - 1
            friends_processed = 0

    return id_to_friends