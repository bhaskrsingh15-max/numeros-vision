"""
Abstract Search Research Provider Interface
Implements Section 3 (Research Connector Layer)
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.seo.research_data_model import ResearchRecord


class SearchResearchProvider(ABC):
    """Abstract base class for all external research providers."""

    @abstractmethod
    def discover(self, seed: str, market: str = "in", language: str = "en", platforms: Optional[List[str]] = None) -> List[ResearchRecord]:
        """Discovers keywords, questions, and variants for a seed topic."""
        pass

    @abstractmethod
    def fetch_metrics(self, keywords: List[str], market: str = "in", language: str = "en") -> Dict[str, Dict[str, Any]]:
        """Fetches search volume, CPC, and competition metrics."""
        pass

    @abstractmethod
    def get_source_metadata(self) -> Dict[str, Any]:
        """Returns provenance, version, and collection metadata."""
        pass

    @abstractmethod
    def get_quota_status(self) -> Dict[str, Any]:
        """Returns current rate limit and quota consumption status."""
        pass
