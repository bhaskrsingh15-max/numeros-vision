"""
Numeros Vision — SEO Engine REST API Router
Implements Section 23 (API Contracts) for automated research, briefs, drafting, publishing, IndexNow, and revenue analytics.
"""

from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import os
import json

from app.seo.connectors.atp_adapter import AnswerThePublicAdapter
from app.seo.connectors.indexnow_adapter import IndexNowAdapter
from app.seo.opportunity_scorer import OpportunityScorer
from app.seo.brief_generator import ContentBriefGenerator
from app.seo.pipeline.content_pipeline import ContentGenerationPipeline
from app.seo.publishing_adapter import WebsitePublishingAdapter
from app.seo.conversion_analytics import ConversionAnalyticsEngine
from app.seo.images.diagram_renderer import DeterministicDiagramRenderer
from app.seo.images.image_service import ImageService
from app.seo.images.media_registry import MediaRegistry

router = APIRouter(prefix="/api/v1/seo-engine", tags=["seo-engine"])

atp_adapter = AnswerThePublicAdapter()
indexnow_adapter = IndexNowAdapter()
brief_gen = ContentBriefGenerator()
pipeline = ContentGenerationPipeline()
publisher = WebsitePublishingAdapter()
analytics = ConversionAnalyticsEngine()
image_service = ImageService()
media_registry = MediaRegistry()

# Pydantic Request Models
class BriefRequest(BaseModel):
    primary_keyword: str
    target_url: str
    intent: str = "INFORMATIONAL"
    page_type: str = "Educational Guide"
    secondary_keywords: List[str] = []
    relevant_offer_id: Optional[str] = None

class PublishRequest(BaseModel):
    slug: str
    html_content: str
    meta_info: Dict[str, Any] = {}
    notify_indexnow: bool = True

class IndexNowRequest(BaseModel):
    urls: List[str]

class TrackEventRequest(BaseModel):
    event_name: str
    canonical_url: str
    properties: Dict[str, Any] = {}
    session_id: Optional[str] = None


@router.post("/research/import-atp")
def import_atp_data(seed: str = "numerology", market: str = "in", language: str = "en"):
    """Imports or refreshes verified AnswerThePublic research records."""
    records = atp_adapter.discover(seed=seed, market=market, language=language)
    metadata = atp_adapter.get_source_metadata()
    return {
        "status": "SUCCESS",
        "total_records_loaded": len(records),
        "source_metadata": metadata,
        "sample_keywords": [r.normalized_keyword for r in records[:5]]
    }


@router.get("/keywords")
def get_keywords(limit: int = 50, cluster: Optional[str] = None):
    """Retrieves verified and prioritized keyword inventory."""
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
    inv_file = os.path.join(data_dir, "keyword_expansion_inventory.json")
    if not os.path.exists(inv_file):
        raise HTTPException(status_code=404, detail="Keyword expansion inventory not found.")
    
    with open(inv_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    records = data.get("records", [])
    if cluster:
        records = [r for r in records if cluster.lower() in r.get("cluster_name", "").lower()]
    return {
        "total": len(records),
        "records": records[:limit]
    }


@router.post("/briefs/generate")
def generate_content_brief(req: BriefRequest):
    """Generates a structured, evidence-grounded content brief."""
    brief = brief_gen.generate_brief(
        primary_keyword=req.primary_keyword,
        target_url=req.target_url,
        intent=req.intent,
        page_type=req.page_type,
        secondary_keywords=req.secondary_keywords,
        relevant_offer_id=req.relevant_offer_id
    )
    return brief.to_dict()


@router.post("/pipeline/run")
def run_content_generation(brief_req: BriefRequest, is_human_approved: bool = True):
    """Executes Stages A through E of the content pipeline and validates quality gates."""
    brief = brief_gen.generate_brief(
        primary_keyword=brief_req.primary_keyword,
        target_url=brief_req.target_url,
        intent=brief_req.intent,
        page_type=brief_req.page_type,
        secondary_keywords=brief_req.secondary_keywords,
        relevant_offer_id=brief_req.relevant_offer_id
    )
    result = pipeline.run_pipeline(brief, is_human_approved=is_human_approved)
    return result


@router.post("/publishing/publish")
def publish_page(req: PublishRequest):
    """Publishes validated HTML content idempotently and notifies IndexNow."""
    result = publisher.publish_page(
        slug=req.slug,
        html_content=req.html_content,
        meta_info=req.meta_info,
        notify_indexnow=req.notify_indexnow
    )
    return result


@router.post("/indexing/submit-indexnow")
def submit_indexnow(req: IndexNowRequest):
    """Submits changed canonical URLs to IndexNow participating engines."""
    result = indexnow_adapter.submit_urls(req.urls)
    return result


@router.post("/analytics/track")
def track_event(req: TrackEventRequest):
    """Records privacy-safe user discovery or engagement event."""
    result = analytics.track_event(
        event_name=req.event_name,
        canonical_url=req.canonical_url,
        properties=req.properties,
        session_id=req.session_id
    )
    return result


@router.get("/analytics/dashboard")
def get_analytics_dashboard():
    """Returns separate discovery, engagement, and confirmed revenue metrics."""
    return analytics.get_funnel_summary()


# ── Automated Visual Media Endpoints (Section 7) ─────────────────────

class DiagramRenderRequest(BaseModel):
    diagram_type: str = "LO_SHU_GRID"
    title: str = "Lo Shu Magic Square Energy Grid"
    subtitle: str = "Traditional 3x3 Planetary Matrix"
    active_numbers: Optional[List[int]] = None
    compound_num: Optional[int] = None
    root_num: Optional[int] = None

class ImageProcessRequest(BaseModel):
    topic: str
    target_keyword: str
    article_url: str
    custom_alt_text: Optional[str] = None
    is_hero: bool = True


@router.post("/images/render-diagram")
def render_diagram(req: DiagramRenderRequest):
    """Renders a deterministic mathematical numerology diagram in SVG format."""
    dtype = req.diagram_type.upper()
    if dtype == "LO_SHU_GRID":
        res = DeterministicDiagramRenderer.render_lo_shu_grid(
            active_numbers=req.active_numbers,
            title=req.title,
            subtitle=req.subtitle
        )
        return {
            "diagram_type": res["diagram_type"],
            "width": res["width"],
            "height": res["height"],
            "content_hash": res["content_hash"],
            "svg": res["svg"]
        }
    elif dtype == "CHALDEAN_MATRIX":
        res = DeterministicDiagramRenderer.render_chaldean_sound_matrix(
            title=req.title,
            subtitle=req.subtitle
        )
        return {
            "diagram_type": res["diagram_type"],
            "width": res["width"],
            "height": res["height"],
            "content_hash": res["content_hash"]
        }
    elif dtype == "COMPOUND_SEAL":
        c_num = req.compound_num or 24
        r_num = req.root_num or ((c_num - 1) % 9 + 1)
        res = DeterministicDiagramRenderer.render_compound_seal(
            compound_num=c_num,
            root_num=r_num,
            title=req.title,
            archetype="Harmonic Synthesis",
            keywords=["Equilibrium", "Integrity", "Leadership"]
        )
        return {
            "diagram_type": res["diagram_type"],
            "compound_num": res["compound_num"],
            "root_num": res["root_num"],
            "content_hash": res["content_hash"]
        }
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported diagram_type '{req.diagram_type}'")


@router.post("/images/process")
def process_image(req: ImageProcessRequest):
    """Generates deterministic visual asset, responsive WebP variants, and registers asset."""
    result = image_service.process_article_visual(
        topic=req.topic,
        target_keyword=req.target_keyword,
        article_url=req.article_url,
        custom_alt_text=req.custom_alt_text,
        is_hero=req.is_hero
    )
    return result


@router.get("/images/media-registry")
def get_media_registry(limit: int = 50, article_url: Optional[str] = None):
    """Retrieves registered visual media assets with full provenance and content hashes."""
    if article_url:
        assets = media_registry.get_assets_by_article(article_url)
    else:
        assets = media_registry.list_all_assets(limit=limit)
    return {
        "total": len(assets),
        "assets": assets
    }

