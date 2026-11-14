# -*- coding: utf-8 -*-
"""
app/logo_intelligence/router.py
===============================
FastAPI Router for Phase 5 Logo Intelligence (`numeros-engine`), authenticated
via `X-NV-Engine-Secret` (`ENGINE_SERVICE_SECRET`).

Endpoints:
1. `POST /api/v1/logo/preview`
2. `POST /api/v1/logo/analyze-existing` (JSON or `multipart/form-data` file upload)
3. `POST /api/v1/logo/five-layer-evaluate` (JSON or `multipart/form-data` file upload)
"""

from __future__ import annotations

from email.parser import BytesParser
from email.policy import default as _email_default_policy
import json
from typing import Any, Callable, Dict, Optional, Tuple

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.logo_intelligence.five_layer_pipeline import (
    LogoInputError,
    run_analyze_existing_endpoint,
    run_five_layer_logo_evaluation,
    run_logo_preview_endpoint,
)

MAX_LOGO_JSON_BYTES = 14 * 1024 * 1024


def _parse_multipart_bytes(
    raw_body: bytes,
    content_type_header: str,
) -> Tuple[Dict[str, Any], Optional[bytes], Optional[str], Optional[str]]:
    """
    RFC 7578 `multipart/form-data` parser using Python standard library `email.parser.BytesParser`
    so multipart file uploads work deterministically even if `python-multipart` is not installed.
    """
    mime_blob = f"Content-Type: {content_type_header}\r\nMIME-Version: 1.0\r\n\r\n".encode("utf-8") + raw_body
    msg = BytesParser(policy=_email_default_policy).parsebytes(mime_blob)
    if not msg.is_multipart():
        raise LogoInputError("Malformed multipart/form-data payload.")

    payload: Dict[str, Any] = {}
    uploaded_bytes: Optional[bytes] = None
    uploaded_filename: Optional[str] = None
    uploaded_mime: Optional[str] = None

    for part in msg.iter_parts():
        field_name = part.get_param("name", header="content-disposition")
        filename = part.get_filename()
        part_bytes = part.get_payload(decode=True) or b""
        if filename is not None:
            uploaded_bytes = part_bytes
            uploaded_filename = filename
            uploaded_mime = part.get_content_type()
        elif field_name:
            val = part_bytes.decode("utf-8", errors="replace")
            if field_name in ("payload_json", "metadata") and val.strip():
                try:
                    parsed_meta = json.loads(val)
                    if isinstance(parsed_meta, dict):
                        payload.update(parsed_meta)
                except Exception as exc:
                    raise LogoInputError("Malformed `payload_json` in multipart form.") from exc
            elif field_name == "partners" and val.strip().startswith("["):
                try:
                    payload[field_name] = json.loads(val)
                except Exception as exc:
                    raise LogoInputError("Malformed `partners` JSON array.") from exc
            elif field_name == "dpdp_consent":
                payload[field_name] = val.strip().lower() in ("true", "1", "yes", "on")
            else:
                payload[field_name] = val

    return payload, uploaded_bytes, uploaded_filename, uploaded_mime


async def _parse_json_or_multipart(
    request: Request,
) -> Tuple[Dict[str, Any], Optional[bytes], Optional[str], Optional[str]]:
    raw_ctype = request.headers.get("content-type") or ""
    ctype = raw_ctype.lower()
    raw = await request.body()
    if len(raw) > MAX_LOGO_JSON_BYTES:
        raise LogoInputError("Logo payload exceeds maximum allowed size.")
    if "multipart/form-data" in ctype:
        return _parse_multipart_bytes(raw, raw_ctype)

    if not raw:
        return {}, None, None, None
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise LogoInputError("Malformed JSON request body.") from exc
    if not isinstance(parsed, dict):
        raise LogoInputError("JSON body must be an object.")
    return parsed, None, None, None


def create_logo_intelligence_router(auth_dep: Callable[[Request], None]) -> APIRouter:
    router = APIRouter(tags=["Logo Intelligence v1"])

    @router.post("/api/v1/logo/preview")
    async def handle_logo_preview(request: Request) -> JSONResponse:
        auth_dep(request)
        try:
            payload, _, _, _ = await _parse_json_or_multipart(request)
            out = run_logo_preview_endpoint(payload)
            return JSONResponse(status_code=200, content=out)
        except LogoInputError as exc:
            return JSONResponse(
                status_code=400,
                content={"ok": False, "code": exc.code, "error": exc.message, "detail": exc.message},
            )

    @router.post("/api/v1/logo/analyze-existing")
    async def handle_logo_analyze_existing(request: Request) -> JSONResponse:
        auth_dep(request)
        try:
            payload, file_bytes, fname, fmime = await _parse_json_or_multipart(request)
            out = run_analyze_existing_endpoint(
                payload,
                uploaded_bytes=file_bytes,
                uploaded_filename=fname,
                uploaded_mime=fmime,
            )
            return JSONResponse(status_code=200, content=out)
        except LogoInputError as exc:
            return JSONResponse(
                status_code=400,
                content={"ok": False, "code": exc.code, "error": exc.message, "detail": exc.message},
            )

    @router.post("/api/v1/logo/five-layer-evaluate")
    async def handle_logo_five_layer_evaluate(request: Request) -> JSONResponse:
        auth_dep(request)
        try:
            payload, file_bytes, fname, fmime = await _parse_json_or_multipart(request)
            out = run_five_layer_logo_evaluation(
                payload,
                uploaded_bytes=file_bytes,
                uploaded_filename=fname,
                uploaded_mime=fmime,
            )
            return JSONResponse(status_code=200, content=out)
        except LogoInputError as exc:
            return JSONResponse(
                status_code=400,
                content={"ok": False, "code": exc.code, "error": exc.message, "detail": exc.message},
            )

    return router
