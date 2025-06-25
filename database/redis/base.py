import redis

class Base:
    def __init__(self):
        self.redis = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=True
        )
    
    def get(self, key):
        if self.redis.exists(key):
            return self.redis.get(key)
        else:
            return None
    
    def set(self, key, value):
        if self.redis.exists(key):
            self.redis.delete(key)
        self.redis.set(key, value)
    
    def delete(self, key):
        if self.redis.exists(key):
            self.redis.delete(key)
        else:
            return None
    
    def exists(self, key):
        return self.redis.exists(key)


base = Base()