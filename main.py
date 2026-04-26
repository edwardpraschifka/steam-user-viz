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
        adj_list = r.json()['friendslist']['friends']
        return adj_list
    else:
        raise RuntimeError(f"Error: {url} responded with code {r.status_code}")

def bfs(user_id, depth=1, process=get_friends):
    """For a given user id and depth, return a dictionary of 
    at most {depth}-degree friends of the user"""

    # dictionary mapping user id's to an array of friends
    adj_list = {}

    # queue of user id's to process
    friend_queue = queue.Queue()

    # track depth
    friends_in_layer = 1
    friends_processed = 0

    # track visited nodes
    visited = {}

    friend_queue.put(user_id)

    while depth > 0 and not friend_queue.empty():
        current_id = friend_queue.get()

        try:
            adj_list[current_id] = process(current_id)
        except:
            adj_list[current_id] = []

        for friend_dict in adj_list[current_id]:
            if friend_dict['steamid'] not in adj_list and friend_dict['steamid'] not in visited:
                friend_queue.put(friend_dict['steamid'])

                visited[friend_dict['steamid']] = True

        friends_processed = friends_processed + 1
        
        if friends_processed == friends_in_layer:
            friends_in_layer = friend_queue.qsize()
            depth = depth - 1
            friends_processed = 0

    return adj_list