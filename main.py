from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from threading import Lock
import time
import threading
from collections import OrderedDict

app = FastAPI(title="SmartCache", description="An Optimized Content Caching System")

# Simulated slow API
def slow_api():
    time.sleep(2)
    return {"data": "Slow API response"}

# In-memory cache class with LRU eviction
class LRUCache:
    def __init__(self, ttl: int = 300, max_size: int = 100):
        self.cache = OrderedDict()
        self.ttl = ttl
        self.max_size = max_size
        self.lock = Lock()
        self.hits = 0
        self.misses = 0

    def get(self, key):
        with self.lock:
            if key in self.cache:
                value, timestamp = self.cache[key]
                if time.time() - timestamp < self.ttl:
                    # Cache hit
                    self.cache.move_to_end(key)
                    self.hits += 1
                    return value
                else:
                    # Cache expired
                    del self.cache[key]
            # Cache miss
            self.misses += 1
            return None

    def set(self, key, value):
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = (value, time.time())
            if len(self.cache) > self.max_size:
                self.cache.popitem(last=False)  # Evict least recently used item

    def invalidate(self, key):
        with self.lock:
            if key in self.cache:
                del self.cache[key]

    def statistics(self):
        with self.lock:
            return {
                "hits": self.hits,
                "misses": self.misses,
                "current_size": len(self.cache),
                "max_size": self.max_size,
                "ttl": self.ttl,
            }

    def update_settings(self, ttl: int = None, max_size: int = None):
        with self.lock:
            if ttl is not None:
                self.ttl = ttl
            if max_size is not None:
                self.max_size = max_size

# Global cache instance
cache = LRUCache()

# Cache stampede prevention lock
stampede_lock = threading.Lock()

@app.get("/content")
async def get_content():
    cache_key = "content"
    cached_content = cache.get(cache_key)
    if cached_content is not None:
        return JSONResponse(content=cached_content)

    with stampede_lock:
        # Double check cache to prevent stampede
        cached_content = cache.get(cache_key)
        if cached_content is not None:
            return JSONResponse(content=cached_content)

        # Fetch from slow API and update cache
        try:
            response = slow_api()
            cache.set(cache_key, response)
            return JSONResponse(content=response)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to fetch content")

@app.post("/invalidate")
async def invalidate_cache(key: str):
    cache.invalidate(key)
    return {"message": f"Cache for key '{key}' invalidated."}

@app.get("/stats")
async def cache_stats():
    return cache.statistics()

class CacheSettings(BaseModel):
    ttl: int = None
    max_size: int = None

@app.post("/settings")
async def update_cache_settings(settings: CacheSettings):
    cache.update_settings(ttl=settings.ttl, max_size=settings.max_size)
    return {"message": "Cache settings updated.", "settings": cache.statistics()}
