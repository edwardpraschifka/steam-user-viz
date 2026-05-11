import time

class Cache:
    def __init__(self, ttl):
        self.ttl = ttl
        self.contents = {
            # key_i: {data: any, cached_at: float}
        }
        self.miss_count = 0
        self.hit_count = 0

    def get(self, key):
        """Fetch key's corresponding value, or None if expired or missing"""

        entry = self.contents.get(key)
        if entry is None or time.time() - entry["cached_at"] > self.ttl:
            self.miss_count = self.miss_count + 1
            return None
        else: 
            self.hit_count = self.hit_count + 1
            return entry["data"]


    def set(self, key, data):
        """Cache (key, data) pair with the current timestamp."""

        self.contents[key] = {"data": data, "cached_at": time.time()}
    
    def total_queries(self):
        """Return sum of misses and hits"""
        
        return self.miss_count + self.hit_count


one_month = 60 * 60 * 24 * 30

# maps ids to friends lists
friends_cache = Cache(ttl=one_month)

# maps ids to player summaries
player_cache = Cache(ttl=one_month)
