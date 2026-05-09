import time

class Cache:
    def __init__(self, ttl):
        self.ttl = ttl
        self.contents = {
            # key_i: {data: any, cached_at: float}
        }

    def get(self, key):
        """Fetch key's corresponding value, or None if expired or missing"""

        entry = self.contents.get(key)
        if entry is None:
            return None
        if time.time() - entry["cached_at"] > self.ttl:
            return None
        return entry["data"]


    def set(self, key, data):
        """Cache (key, data) pair with the current timestamp."""

        self.contents[key] = {"data": data, "cached_at": time.time()}


one_month = 60 * 60 * 24 * 30

# maps ids to friends lists
friends_cache = Cache(ttl=one_month)

# maps ids to player summaries
player_cache = Cache(ttl=one_month)
