"""
Bing IndexNow Provider Adapter
Implements Section 3.5 & Section 18 (Indexing and Discovery Automation)
"""

import os
import json
import logging
import datetime
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional

logger = logging.getLogger("indexnow_adapter")

class IndexNowAdapter:
    """Submits canonical URLs to Bing and participating search engines via IndexNow."""

    ENDPOINT = "https://api.indexnow.org/indexnow"
    DEFAULT_HOST = "numerosvision.com"

    def __init__(self, key: Optional[str] = None, host: Optional[str] = None):
        self.host = host or os.getenv("INDEXNOW_HOST", self.DEFAULT_HOST)
        # 32-character hexadecimal key (or environment variable)
        self.key = key or os.getenv("INDEXNOW_KEY", "numerosvision2026indexnowkey32c")
        self.key_location = f"https://{self.host}/{self.key}.txt"
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data"))
        self.log_file = os.path.join(self.data_dir, "indexing_events.jsonl")

    def submit_urls(self, url_list: List[str]) -> Dict[str, Any]:
        """
        Submits changed canonical URLs to IndexNow.
        Returns the submission response and logs the event.
        """
        if not url_list:
            return {"status": "EMPTY_LIST", "submitted_count": 0}

        # Filter and sanitize URLs
        clean_urls = []
        for u in url_list:
            if not u.startswith("http"):
                clean_urls.append(f"https://{self.host}{u if u.startswith('/') else '/' + u}")
            else:
                clean_urls.append(u)

        payload = {
            "host": self.host,
            "key": self.key,
            "keyLocation": self.key_location,
            "urlList": clean_urls
        }

        json_bytes = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json; charset=utf-8"}
        req = urllib.request.Request(self.ENDPOINT, data=json_bytes, headers=headers, method="POST")

        timestamp = datetime.datetime.now().isoformat()
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                code = resp.getcode()
                response_text = resp.read().decode("utf-8") if resp.length else "OK"
                result = {
                    "status": "SUBMISSION_ACCEPTED" if code in (200, 202) else f"HTTP_{code}",
                    "http_status": code,
                    "response": response_text,
                    "submitted_urls": clean_urls,
                    "timestamp": timestamp
                }
        except urllib.error.HTTPError as e:
            result = {
                "status": f"HTTP_ERROR_{e.code}",
                "http_status": e.code,
                "error": str(e.reason),
                "submitted_urls": clean_urls,
                "timestamp": timestamp
            }
        except Exception as e:
            result = {
                "status": "CLIENT_NETWORK_ERROR",
                "http_status": None,
                "error": str(e),
                "submitted_urls": clean_urls,
                "timestamp": timestamp
            }

        # Append to audit log
        self._log_event(result)
        return result

    def _log_event(self, event_data: Dict[str, Any]):
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(event_data) + "\n")
        except Exception as e:
            logger.error(f"Failed to log IndexNow event: {e}")

    def get_submission_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Reads recent indexing submission events."""
        if not os.path.exists(self.log_file):
            return []
        events = []
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        events.append(json.loads(line))
        except Exception as e:
            logger.error(f"Failed to read IndexNow history: {e}")
        return events[-limit:]
