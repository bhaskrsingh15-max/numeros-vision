"""
ZERO-COST IN-MEMORY LRU CACHE SERVICE
Caches deterministic chart calculations and consensus readings in RAM.
Serves repeated requests in <1ms without recomputation, saving CPU and RAG lookup overhead at $0 cost.
"""

import hashlib
import json
import time
from typing import Dict, Any, Optional

class LRUCacheService:
    def __init__(self, capacity: int = 1000, ttl_seconds: int = 86400):
        self.capacity = capacity
        self.ttl_seconds = ttl_seconds
        self.cache: Dict[str, Tuple[float, Any]] = {}

    def _make_key(self, day: int, month: int, year: int, extra: str = "") -> str:
        raw_key = f"{day:02d}-{month:02d}-{year}:{extra}"
        return hashlib.sha256(raw_key.encode('utf-8')).hexdigest()

    def get(self, day: int, month: int, year: int, extra: str = "") -> Optional[Any]:
        key = self._make_key(day, month, year, extra)
        if key in self.cache:
            created_at, val = self.cache[key]
            if time.time() - created_at < self.ttl_seconds:
                return val
            else:
                del self.cache[key]  # Expired TTL
        return None

    def set(self, day: int, month: int, year: int, val: Any, extra: str = ""):
        if len(self.cache) >= self.capacity:
            # Evict oldest entry (LRU simple FIFO/TTL clear)
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][0])
            del self.cache[oldest_key]
            
        key = self._make_key(day, month, year, extra)
        self.cache[key] = (time.time(), val)

    def stats(self) -> Dict[str, Any]:
        return {
            "cached_entries_count": len(self.cache),
            "max_capacity": self.capacity,
            "ttl_seconds": self.ttl_seconds
        }

# Global singleton cache instance
calculation_cache = LRUCacheService()
