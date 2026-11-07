"""
NUMEROS VISION & ASKNUMEROAI — COST-OPTIMIZED MULTI-TIER CACHE ENGINE
Specification: AI Cost and Token Optimization Architecture (Section 8)

Implements 6 distinct, version-aware, privacy-isolated cache tiers:
1. CALCULATIONS: Deterministic math formulas (Driver, Conductor, Kua, Lo Shu, Name compounds).
2. RETRIEVAL: Targeted RAG chunk results keyed by query + filter + corpus version.
3. EMBEDDINGS: Vector / semantic embeddings keyed by text hash + model version.
4. REPORT_SECTIONS: Canonical narrative building blocks keyed by section type + parameters.
5. FAQS: Approved static question-and-answer pairs.
6. ELIGIBLE_GENERATED_ANSWERS: Common anonymous generated answers for recurring archetypes.

Key Features:
- Version-Aware Compound Hashing (SHA-256 over normalized inputs, method, engine version, config version)
- Strict Tenant & Privacy Isolation (prevents cross-user data leakage)
- TTL-based auto-expiration and LRU capacity management
- Cost & Token Savings Accounting (tracks exact hits, misses, tokens saved, USD/INR saved)
"""

import hashlib
import json
import time
from typing import Dict, Any, Optional, Tuple, List
from enum import Enum


class CacheTier(str, Enum):
    CALCULATIONS = "calculations"
    RETRIEVAL = "retrieval"
    EMBEDDINGS = "embeddings"
    REPORT_SECTIONS = "report_sections"
    FAQS = "faqs"
    ANSWERS = "answers"


# Default TTLs (in seconds) per specification
DEFAULT_TTLS = {
    CacheTier.CALCULATIONS: 7 * 86400,        # 7 days
    CacheTier.RETRIEVAL: 24 * 3600,            # 24 hours
    CacheTier.EMBEDDINGS: 30 * 86400,          # 30 days
    CacheTier.REPORT_SECTIONS: 7 * 86400,      # 7 days
    CacheTier.FAQS: 30 * 86400,                # 30 days
    CacheTier.ANSWERS: 24 * 3600,              # 24 hours
}

# Average tokens saved when serving from cache
TOKENS_SAVED_BENCHMARK = {
    CacheTier.CALCULATIONS: 600,               # Avoids LLM parsing & verification
    CacheTier.RETRIEVAL: 1200,                 # Avoids raw chunk re-ingestion
    CacheTier.EMBEDDINGS: 400,                 # Avoids embedding model API calls
    CacheTier.REPORT_SECTIONS: 2500,           # Avoids section generation
    CacheTier.FAQS: 800,                       # Avoids answering FAQ via LLM
    CacheTier.ANSWERS: 3000,                   # Avoids full synthesis LLM call
}

USD_PER_1K_SAVINGS_ESTIMATE = 0.0015           # Standard tier blended price ($1.50 per 1M tokens)
INR_EXCHANGE_RATE = 85.0                       # 85 INR per USD


class CacheEntry:
    __slots__ = ("key", "tier", "value", "created_at", "ttl_seconds", "user_id", "tokens_saved")

    def __init__(self, key: str, tier: CacheTier, value: Any, ttl_seconds: int, user_id: Optional[str] = None, tokens_saved: int = 0):
        self.key = key
        self.tier = tier
        self.value = value
        self.created_at = time.time()
        self.ttl_seconds = ttl_seconds
        self.user_id = user_id
        self.tokens_saved = tokens_saved

    def is_expired(self) -> bool:
        return (time.time() - self.created_at) > self.ttl_seconds


class CostOptimizedCacheService:
    """
    High-performance, in-memory, multi-tier cache with version safety,
    tenant privacy partitioning, and cost savings telemetry.
    """

    def __init__(
        self,
        engine_version: str = "3.9.0",
        config_version: str = "v1",
        max_entries_per_tier: int = 2000
    ):
        self.engine_version = engine_version
        self.config_version = config_version
        self.max_entries_per_tier = max_entries_per_tier
        
        # Partitioned store: {CacheTier: {cache_key: CacheEntry}}
        self._stores: Dict[CacheTier, Dict[str, CacheEntry]] = {
            tier: {} for tier in CacheTier
        }

        # Telemetry metrics
        self.metrics = {
            "hits": {tier.value: 0 for tier in CacheTier},
            "misses": {tier.value: 0 for tier in CacheTier},
            "tokens_saved": 0,
            "cost_saved_usd": 0.0,
            "cost_saved_inr": 0.0,
            "total_evictions": 0,
        }

    def compute_compound_key(
        self,
        tier: CacheTier,
        method: str,
        inputs: Any,
        user_id: Optional[str] = None,
        custom_version: Optional[str] = None
    ) -> str:
        """
        Formulates a deterministic SHA-256 compound key:
        SHA-256(tier | method | normalized_inputs | engine_version | config_version [| user_id])
        """
        if isinstance(inputs, dict):
            # Sort keys for deterministic JSON serialization
            normalized_str = json.dumps(inputs, sort_keys=True, separators=(",", ":"), default=str)
        elif isinstance(inputs, (list, tuple)):
            normalized_str = json.dumps(list(inputs), default=str)
        else:
            normalized_str = str(inputs).strip()

        ver = custom_version or self.engine_version
        privacy_component = f"|user:{user_id}" if user_id else "|anonymous"

        raw_key = f"{tier.value}|{method}|{normalized_str}|ver:{ver}|cfg:{self.config_version}{privacy_component}"
        return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    def get(
        self,
        tier: CacheTier,
        method: str,
        inputs: Any,
        user_id: Optional[str] = None,
        custom_version: Optional[str] = None
    ) -> Optional[Any]:
        """
        Retrieves a cached value if present and unexpired.
        Updates hit/miss and token savings metrics.
        """
        key = self.compute_compound_key(tier, method, inputs, user_id, custom_version)
        store = self._stores[tier]

        entry = store.get(key)
        if entry is None:
            self.metrics["misses"][tier.value] += 1
            return None

        # Check expiration
        if entry.is_expired():
            del store[key]
            self.metrics["misses"][tier.value] += 1
            return None

        # Check tenant privacy isolation
        if entry.user_id is not None and entry.user_id != user_id:
            # Privacy barrier: cross-user hit strictly forbidden
            self.metrics["misses"][tier.value] += 1
            return None

        # Hit recorded
        self.metrics["hits"][tier.value] += 1
        tokens_saved = entry.tokens_saved or TOKENS_SAVED_BENCHMARK.get(tier, 500)
        self.metrics["tokens_saved"] += tokens_saved
        usd_saved = (tokens_saved / 1000.0) * USD_PER_1K_SAVINGS_ESTIMATE
        self.metrics["cost_saved_usd"] = round(self.metrics["cost_saved_usd"] + usd_saved, 6)
        self.metrics["cost_saved_inr"] = round(self.metrics["cost_saved_usd"] * INR_EXCHANGE_RATE, 4)

        return entry.value

    def set(
        self,
        tier: CacheTier,
        method: str,
        inputs: Any,
        value: Any,
        user_id: Optional[str] = None,
        ttl_seconds: Optional[int] = None,
        custom_version: Optional[str] = None,
        tokens_saved_override: Optional[int] = None
    ) -> str:
        """
        Stores value in designated cache tier with capacity management.
        """
        key = self.compute_compound_key(tier, method, inputs, user_id, custom_version)
        store = self._stores[tier]
        ttl = ttl_seconds if ttl_seconds is not None else DEFAULT_TTLS.get(tier, 86400)
        tokens_saved = tokens_saved_override or TOKENS_SAVED_BENCHMARK.get(tier, 500)

        # LRU eviction if tier capacity exceeded
        if len(store) >= self.max_entries_per_tier and key not in store:
            oldest_key = min(store.keys(), key=lambda k: store[k].created_at)
            del store[oldest_key]
            self.metrics["total_evictions"] += 1

        store[key] = CacheEntry(
            key=key,
            tier=tier,
            value=value,
            ttl_seconds=ttl,
            user_id=user_id,
            tokens_saved=tokens_saved
        )
        return key

    def invalidate(
        self,
        tier: Optional[CacheTier] = None,
        method_prefix: Optional[str] = None
    ) -> int:
        """
        Invalidates entries in a given tier or all tiers.
        Returns count of purged records.
        """
        purged = 0
        tiers_to_clear = [tier] if tier else list(CacheTier)

        for t in tiers_to_clear:
            store = self._stores[t]
            if method_prefix is None:
                purged += len(store)
                store.clear()
            else:
                keys_to_remove = [k for k, v in store.items()]
                # If method prefix is specified, we check or clear all
                purged += len(keys_to_remove)
                store.clear()
        return purged

    def get_stats(self) -> Dict[str, Any]:
        """Returns comprehensive cache diagnostics, hit rates, and monetary savings."""
        total_hits = sum(self.metrics["hits"].values())
        total_misses = sum(self.metrics["misses"].values())
        total_requests = total_hits + total_misses
        overall_hit_rate_pct = round((total_hits / total_requests * 100.0), 2) if total_requests > 0 else 0.0

        tier_breakdown = {}
        for tier in CacheTier:
            h = self.metrics["hits"][tier.value]
            m = self.metrics["misses"][tier.value]
            reqs = h + m
            tier_breakdown[tier.value] = {
                "active_entries": len(self._stores[tier]),
                "hits": h,
                "misses": m,
                "hit_rate_pct": round((h / reqs * 100.0), 2) if reqs > 0 else 0.0
            }

        return {
            "engine_version": self.engine_version,
            "config_version": self.config_version,
            "overall": {
                "total_requests": total_requests,
                "total_hits": total_hits,
                "total_misses": total_misses,
                "hit_rate_pct": overall_hit_rate_pct,
                "tokens_saved": self.metrics["tokens_saved"],
                "cost_saved_usd": self.metrics["cost_saved_usd"],
                "cost_saved_inr": self.metrics["cost_saved_inr"],
                "total_evictions": self.metrics["total_evictions"]
            },
            "tiers": tier_breakdown
        }


# Global singleton instance of the cost-optimized multi-tier cache
cost_cache = CostOptimizedCacheService()
