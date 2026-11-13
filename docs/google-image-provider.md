# Numeros Vision — Google GenAI Image Provider Integration Specification
**Document Version**: 1.0.0  
**Effective Date**: 2026-10-21  
**Integration Target**: Google GenAI / Gemini Image Generation (`imagen-3.0-generate-002`)  
**Official Documentation Reference**:
- Image generation and editing: `https://ai.google.dev/gemini-api/docs/image-generation`
- Gemini 3 developer guide: `https://ai.google.dev/gemini-api/docs/gemini-3`
- Official changelog: `https://ai.google.dev/gemini-api/docs/changelog`

---

## 1. Provider Adapter Architecture

To insulate the platform from vendor SDK shifts and protect server credentials, Numeros Vision employs a strict server-side provider adapter (`app/services/image_provider.py`).

### 1.1 Request & Response Type Contracts

```python
from dataclasses import dataclass, field
from typing import List, Optional, Literal

@dataclass
class ImageReference:
    asset_id: str
    mime_type: str
    purpose: Literal["existing_logo", "style_reference", "customer_sketch"]

@dataclass
class ImageGenerationRequest:
    job_id: str
    prompt: str
    aspect_ratio: Literal["1:1", "4:3", "3:2", "16:9", "9:16"] = "1:1"
    image_size: Literal["512", "1K", "2K", "4K"] = "1K"
    output_count: int = 1
    safety_profile: str = "block_medium_and_above"
    reference_images: List[ImageReference] = field(default_factory=list)

@dataclass
class GeneratedOutput:
    temporary_asset_id: str
    mime_type: str
    width: int
    height: int
    image_bytes: Optional[bytes] = None
    file_path: Optional[str] = None

@dataclass
class ImageGenerationResult:
    provider: str  # "google" or "mock"
    model_id: str
    provider_request_id: Optional[str]
    outputs: List[GeneratedOutput]
    estimated_cost_cents: int
    warnings: List[str] = field(default_factory=list)
```

---

## 2. Server-Side Configuration & Security

- **Environment Variable**: `GOOGLE_GENAI_API_KEY` (Stored strictly server-side).
- **Configurable Model ID**: `GOOGLE_IMAGE_MODEL_ID=imagen-3.0-generate-002`.
- **Timeouts & Retries**: 45-second HTTP timeout; maximum 2 exponential backoff retries on transient 503/429 errors.
- **Fail-Safe Offline Mode**: If `GOOGLE_GENAI_API_KEY` is unset or running in offline unit tests, the adapter seamlessly switches to deterministic synthetic asset generation or vector typesetting without throwing unhandled exceptions.

---

## 3. Provider Verification Smoke Test

Before enabling paid customer generation:
1. Initialize `GoogleImageProvider(api_key=None, mock_mode=True)` and verify mock generation completes in < 50ms with valid PNG/SVG bytes.
2. When credentials are provided, run `scripts/smoke_test_image_provider.py` to confirm model connectivity, response schema conformity, and quota reporting.
3. Validate that no image generation prompt contains raw RAG passages or unapproved traditional claims.
