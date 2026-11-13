"""
Website Publishing Adapter
Implements Section 17 (CMS & Website Publishing Adapter) with revision history, rollback, and IndexNow notifications.
"""

import os
import json
import logging
import datetime
from typing import Dict, Any, Optional
from app.seo.connectors.indexnow_adapter import IndexNowAdapter

logger = logging.getLogger("publishing_adapter")

class WebsitePublishingAdapter:
    """Manages idempotent publishing, revisions, rollbacks, and discovery triggers."""

    def __init__(self):
        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self.static_blog_dir = os.path.join(self.root_dir, "app", "static", "blog")
        self.data_dir = os.path.join(self.root_dir, "data")
        self.revisions_file = os.path.join(self.data_dir, "publishing_revisions.jsonl")
        self.page_registry_file = os.path.join(self.data_dir, "seo_page_registry.json")
        self.indexnow = IndexNowAdapter()
        os.makedirs(self.static_blog_dir, exist_ok=True)

    def publish_page(self, 
                     slug: str, 
                     html_content: str, 
                     meta_info: Dict[str, Any],
                     notify_indexnow: bool = True) -> Dict[str, Any]:
        """
        Publishes a validated HTML page into the live static system idempotently.
        """
        clean_slug = slug.strip("/").split("/")[-1]
        target_file = os.path.join(self.static_blog_dir, f"{clean_slug}.html")
        canonical_url = f"https://numerosvision.com/blog/{clean_slug}"
        timestamp = datetime.datetime.now().isoformat()

        # Check existing revision for rollback capability
        old_content = ""
        if os.path.exists(target_file):
            try:
                with open(target_file, "r", encoding="utf-8") as f:
                    old_content = f.read()
            except Exception as e:
                logger.warning(f"Could not read existing file for rollback backup: {e}")

        # Write new content
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Log revision
        revision_record = {
            "slug": clean_slug,
            "canonical_url": canonical_url,
            "target_file": target_file,
            "published_at": timestamp,
            "content_length": len(html_content),
            "had_previous_version": bool(old_content),
            "meta_info": meta_info,
            "status": "PUBLISHED"
        }
        self._log_revision(revision_record)

        # Update sitemap/page registry
        self._update_page_registry(clean_slug, canonical_url, meta_info)

        # Trigger IndexNow notification if requested
        indexnow_result = None
        if notify_indexnow:
            indexnow_result = self.indexnow.submit_urls([canonical_url])

        return {
            "status": "SUCCESS",
            "published_url": canonical_url,
            "file_path": target_file,
            "timestamp": timestamp,
            "indexnow_notification": indexnow_result
        }

    def rollback_page(self, slug: str, previous_html: str) -> Dict[str, Any]:
        """Rolls back a page to its previous revision."""
        clean_slug = slug.strip("/").split("/")[-1]
        target_file = os.path.join(self.static_blog_dir, f"{clean_slug}.html")
        if not previous_html:
            return {"status": "ERROR", "message": "No previous HTML content provided for rollback."}

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(previous_html)

        timestamp = datetime.datetime.now().isoformat()
        self._log_revision({
            "slug": clean_slug,
            "published_at": timestamp,
            "status": "ROLLED_BACK"
        })
        return {"status": "ROLLED_BACK", "slug": clean_slug, "timestamp": timestamp}

    def _log_revision(self, record: Dict[str, Any]):
        try:
            with open(self.revisions_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")
        except Exception as e:
            logger.error(f"Failed to log revision: {e}")

    def _update_page_registry(self, slug: str, canonical_url: str, meta: Dict[str, Any]):
        try:
            pages = []
            if os.path.exists(self.page_registry_file):
                with open(self.page_registry_file, "r", encoding="utf-8") as f:
                    pages = json.load(f)
            
            # Upsert
            existing = [p for p in pages if p.get("route") == f"/blog/{slug}"]
            if existing:
                existing[0]["status"] = "LIVE"
                existing[0]["updated_at"] = datetime.datetime.now().isoformat()
            else:
                pages.append({
                    "page_number": len(pages) + 1,
                    "route": f"/blog/{slug}",
                    "page_name": meta.get("title", slug.replace("-", " ").title()),
                    "status": "LIVE",
                    "title": meta.get("meta_title", ""),
                    "meta_description": meta.get("meta_description", ""),
                    "h1": meta.get("h1", ""),
                    "primary_keyword": meta.get("primary_keyword", ""),
                    "canonical": canonical_url,
                    "robots": "index,follow"
                })
            with open(self.page_registry_file, "w", encoding="utf-8") as f:
                json.dump(pages, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to update page registry: {e}")
