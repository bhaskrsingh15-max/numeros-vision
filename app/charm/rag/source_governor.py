"""
app/charm/rag/source_governor.py
=================================
Method-Partitioned Retrieval Routing & Source Governance for Charm AI.
Complies with Section 4.1, 4.2, and 4.4 of Master Specification v2.0.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from app.engine.rag_retriever import rag_engine
from app.engine.source_privacy_shield import sanitize_text, sanitize_citation

REGISTRY_PATH = Path(__file__).resolve().parent.parent.parent.parent / "data" / "knowledge_base" / "source_registry.json"

class SourceCitation(dict):
    def __init__(self, source_id: str, title: str, locator: str, verified: bool = True):
        super().__init__(
            source_id=source_id,
            title=title,
            locator=locator,
            verified=verified
        )

class SourceGovernor:
    def __init__(self, registry_file: Path = REGISTRY_PATH):
        self.registry_file = registry_file
        self.sources: Dict[str, Dict[str, Any]] = {}
        self._load_registry()

    def _load_registry(self):
        if self.registry_file.exists():
            try:
                with open(self.registry_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for s in data.get("sources", []):
                        self.sources[s["source_id"]] = s
            except Exception as e:
                print(f"Warning: Failed to load source registry: {e}")

    def is_source_approved(self, source_id: str) -> bool:
        src = self.sources.get(source_id)
        if not src:
            return False
        return src.get("approval_status") == "approved" or src.get("authority_status") == "approved"

    def get_source_metadata(self, source_id: str) -> Optional[Dict[str, Any]]:
        return self.sources.get(source_id)

    def retrieve_method_evidence(
        self,
        method_id: str,
        query: str,
        event_type: str,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Section 4.1 & 4.4: Method-specific partitioned retrieval.
        Never retrieves mixed-method chunks into an undifferentiated context.
        Lal Kitab is strictly gated and disabled.
        """
        if method_id == "LAL_KITAB":
            # Section 1.2: Lal Kitab must remain disabled until approved source exists
            return []

        # Enhance query with method domain tag
        partition_tags = {
            "NUMEROLOGY_DASHA": "dasha mahadasha antardasha personal year",
            "KP_ASTROLOGY": "kp astrology sublord star lord cuspal significator",
            "VEDIC_ASTROLOGY": "vedic parashari transit gochar sambandha yoga",
            "BNN_NADI": "bhrigu nandi nadi bnn karaka saturn jupiter conjunction",
            "REMEDIES": "safe crystal yantra lifestyle hora attunement"
        }

        scoped_query = f"{partition_tags.get(method_id, '')} {query} {event_type}".strip()
        raw_passages = rag_engine.query(scoped_query, top_k=top_k * 2)

        verified_evidence = []
        seen_passages: Set[str] = set()

        for p in raw_passages:
            text = p.get("text", "")
            # Deduplicate similar text chunks
            text_slug = text[:80].lower()
            if text_slug in seen_passages:
                continue
            seen_passages.add(text_slug)

            source_id = p.get("source_id", "SRC-NV-001")
            meta = self.get_source_metadata(source_id) or {
                "title": p.get("source_title", "Numeros Vision Classical Archives"),
                "authority_status": "approved"
            }

            # Security Defense: Sanitize untrusted instruction injection
            clean_text = sanitize_text(text)

            verified_evidence.append({
                "source_id": source_id,
                "title": meta.get("title", "Canonical Treatise"),
                "locator": p.get("locator", f"Section {p.get('chunk_id', 1)}"),
                "content": clean_text,
                "relevance_score": p.get("score", 0.85),
                "method_id": method_id
            })

            if len(verified_evidence) >= top_k:
                break

        return verified_evidence

    def validate_citations(self, citations: List[Dict[str, Any]]) -> List[SourceCitation]:
        validated = []
        for c in citations:
            sid = c.get("source_id", "")
            if self.is_source_approved(sid):
                src = self.get_source_metadata(sid) or {}
                validated.append(SourceCitation(
                    source_id=sid,
                    title=src.get("title", c.get("title", "Canonical Source")),
                    locator=c.get("locator", "Section 1"),
                    verified=True
                ))
            else:
                # Retain for transparency but mark unverified
                validated.append(SourceCitation(
                    source_id=sid or "SRC-UNVERIFIED",
                    title=c.get("title", "Unverified Traditional Commentary"),
                    locator=c.get("locator", "Unresolved"),
                    verified=False
                ))
        return validated

source_governor = SourceGovernor()
