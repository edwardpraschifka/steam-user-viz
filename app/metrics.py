import time
from .cache import friends_cache, player_cache

api_call_count = 0
last_api_call = {}

def get_metrics():
    
    return {
        "time": time.time(),
        "api_call_count": api_call_count,
        "cache_hit_rate": {
            "friends_cache": str(100*friends_cache.hit_count/friends_cache.total_queries()) + "%" if friends_cache.total_queries() > 0 else "0%",
            "player_cache": str(100*player_cache.hit_count/player_cache.total_queries()) + "%" if player_cache.total_queries() > 0 else "0%"
        },
        "last_api_call": last_api_call
    }