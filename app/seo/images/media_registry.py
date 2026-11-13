"""
app.seo.images.media_registry
Persistent Registry and Provenance Ledger for Numeros Vision Visual Assets.

Implements Sections 7.3 and 21 (Images Data Integrity and Traceability):
- Content hashing (SHA-256) for deduplication
- Full provenance recording (DETERMINISTIC_RENDERER, BRAND_ASSET_REPOSITORY)
- Association with target canonical articles
- File size, format, dimension, and accessibility audit status
"""

import os
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

logger = logging.getLogger("media_registry")

class MediaRegistry:
    """Manages the media asset registry JSON ledger."""

    def __init__(self, registry_path: Optional[str] = None):
        if registry_path:
            self.registry_path = registry_path
        else:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data"))
            self.registry_path = os.path.join(base_dir, "media_registry.json")
        self._ensure_registry_exists()

    def _ensure_registry_exists(self):
        os.makedirs(os.path.dirname(self.registry_path), exist_ok=True)
        if not os.path.exists(self.registry_path):
            initial_data = {
                "schema_version": "1.0",
                "description": "Numeros Vision Visual Media Registry & Provenance Ledger",
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "assets": []
            }
            with open(self.registry_path, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, indent=2)

    def _load_data(self) -> Dict[str, Any]:
        try:
            with open(self.registry_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading media registry: {e}")
            return {"assets": []}

    def _save_data(self, data: Dict[str, Any]):
        data["last_updated"] = datetime.now(timezone.utc).isoformat()
        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def register_asset(
        self,
        media_id: str,
        seo_filename: str,
        image_purpose: str,
        associated_article_url: str,
        alt_text: str,
        provenance: str,
        dimensions: Dict[str, List[int]],
        formats: List[str],
        content_hash: str,
        published_variants: Dict[str, Any],
        caption: str = "",
        credit: str = "Numeros Vision Deterministic System",
        accessibility_reviewed: bool = True
    ) -> Dict[str, Any]:
        """
        Registers a media asset. If content_hash exists, returns existing entry to prevent duplication.
        """
        data = self._load_data()
        assets = data.get("assets", [])

        # Deduplication check by content hash
        for item in assets:
            if item.get("content_hash") == content_hash:
                logger.info(f"Asset with content hash {content_hash} already registered as {item.get('media_id')}")
                return item

        total_bytes = sum(
            var_data.get("webp", {}).get("size_bytes", 0) + var_data.get("png", {}).get("size_bytes", 0)
            for var_data in published_variants.values()
        )

        entry = {
            "media_id": media_id,
            "seo_filename": seo_filename,
            "image_purpose": image_purpose,
            "associated_article_url": associated_article_url,
            "alt_text": alt_text,
            "caption": caption,
            "credit": credit,
            "provenance": provenance,
            "dimensions": dimensions,
            "formats": formats,
            "total_size_bytes": total_bytes,
            "content_hash": content_hash,
            "accessibility_reviewed": accessibility_reviewed,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "variants": published_variants
        }

        assets.append(entry)
        data["assets"] = assets
        self._save_data(data)
        logger.info(f"Successfully registered media asset {media_id} ({seo_filename})")
        return entry

    def get_asset_by_id(self, media_id: str) -> Optional[Dict[str, Any]]:
        data = self._load_data()
        for item in data.get("assets", []):
            if item.get("media_id") == media_id:
                return item
        return None

    def get_assets_by_article(self, article_url: str) -> List[Dict[str, Any]]:
        data = self._load_data()
        return [item for item in data.get("assets", []) if item.get("associated_article_url") == article_url]

    def list_all_assets(self, limit: int = 100) -> List[Dict[str, Any]]:
        data = self._load_data()
        return data.get("assets", [])[:limit]
