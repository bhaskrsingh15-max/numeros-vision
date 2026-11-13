# -*- coding: utf-8 -*-
"""
app/services/internal_engine_service.py
=======================================
Numeros Vision Deterministic Python Engine Service (`numeros-engine`).

Serves:
- Charm AI deterministic consultations (`/api/charm/chat`, `/api/charm/chat/stream`, `/api/v1/health/charm`)
  authenticated via `X-NV-Charm-Secret`.
- Phase 4 & Phase 5 deterministic tool & Logo Intelligence services
  authenticated via `X-NV-Engine-Secret`.
"""

from __future__ import annotations

import asyncio
import hmac
import json
import os
import queue
import threading
from typing import Any, Dict, Optional, Tuple

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response, StreamingResponse

from app.services.charm_deterministic_service import (
    SWISSEPH_AVAILABLE,
    CharmInputError,
    run_deterministic_charm_consultation,
    validate_and_parse_charm_input,
)

MAX_CHARM_BODY_BYTES = 65536

app = FastAPI(
    title="Numeros Vision Deterministic Engine Service",
    docs_url=None,
    redoc_url=None,
)


def verify_shared_secret_header(
    request: Request,
    *,
    env_var_name: str,
    header_name: str,
) -> None:
    """
    Fail-closed constant-time header authentication.
    Allows unauthenticated local unit testing ONLY when `NV_ALLOW_UNAUTHENTICATED_LOCAL=true`
    and `ENVIRONMENT` is not `production` or `preview`.
    """
    env_mode = (os.getenv("ENVIRONMENT") or "").strip().lower()
    allow_local = (os.getenv("NV_ALLOW_UNAUTHENTICATED_LOCAL") or "").strip().lower() in {"true", "1"}
    if allow_local and env_mode not in {"production", "preview"}:
        return

    expected = (os.getenv(env_var_name) or "").strip()
    if not expected:
        raise HTTPException(
            status_code=503,
            detail=f"{env_var_name} is not configured on numeros-engine.",
        )

    provided = (request.headers.get(header_name) or "").strip()
    if not provided or not hmac.compare_digest(provided, expected):
        raise HTTPException(
            status_code=403,
            detail="Access denied: invalid or missing service authorization header.",
        )


def verify_charm_secret(request: Request) -> None:
    verify_shared_secret_header(
        request,
        env_var_name="CHARM_SERVICE_SECRET",
        header_name="X-NV-Charm-Secret",
    )


def verify_engine_secret(request: Request) -> None:
    verify_shared_secret_header(
        request,
        env_var_name="ENGINE_SERVICE_SECRET",
        header_name="X-NV-Engine-Secret",
    )


@app.get("/health")
@app.get("/healthz")
@app.get("/internal/v1/health")
@app.get("/api/v1/health/charm")
async def handle_health() -> Dict[str, Any]:
    return {
        "ok": True,
        "status": "ok",
        "service": "numeros-engine",
        "swisseph_available": SWISSEPH_AVAILABLE,
    }


async def _parse_json_body(request: Request, max_bytes: int = MAX_CHARM_BODY_BYTES) -> Dict[str, Any]:
    raw = await request.body()
    if len(raw) > max_bytes:
        raise HTTPException(status_code=413, detail="Request payload exceeds maximum allowed size.")
    if not raw:
        return {}
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Malformed JSON body.") from exc
    if not isinstance(parsed, dict):
        raise HTTPException(status_code=400, detail="JSON body must be an object.")
    return parsed


@app.post("/api/charm/chat")
async def handle_charm_chat(request: Request):
    verify_charm_secret(request)
    payload = await _parse_json_body(request)
    entitlement = str(
        payload.get("_charm_entitlement")
        or request.headers.get("X-NV-Charm-Tier")
        or "charm_free"
    ).strip()

    try:
        result = run_deterministic_charm_consultation(
            payload,
            entitlement_tier=entitlement,
        )
    except CharmInputError as exc:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "status": "INSUFFICIENT_EVIDENCE",
                "code": exc.code,
                "error": exc.message,
                "credit_chargeable": False,
            },
        )
    return JSONResponse(status_code=200, content=result)


@app.post("/api/charm/chat/stream")
async def handle_charm_chat_stream(request: Request):
    verify_charm_secret(request)
    payload = await _parse_json_body(request)
    entitlement = str(
        payload.get("_charm_entitlement")
        or request.headers.get("X-NV-Charm-Tier")
        or "charm_free"
    ).strip()

    # Validate upfront so missing DOB or missing question returns HTTP 400 immediately
    try:
        validate_and_parse_charm_input(payload)
    except CharmInputError as exc:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "status": "INSUFFICIENT_EVIDENCE",
                "code": exc.code,
                "error": exc.message,
                "credit_chargeable": False,
            },
        )

    try:
        running_loop: Optional[asyncio.AbstractEventLoop] = asyncio.get_running_loop()
    except RuntimeError:
        running_loop = None

    if running_loop is None:
        stage_events_buf = []
        result_payload = run_deterministic_charm_consultation(
            payload,
            entitlement_tier=entitlement,
            on_stage=stage_events_buf.append,
        )
        frames = [
            f"event: stage\ndata: {json.dumps(ev, ensure_ascii=False)}\n\n"
            for ev in stage_events_buf
        ]
        frames.append(f"event: result\ndata: {json.dumps(result_payload, ensure_ascii=False)}\n\n")
        return Response(
            content="".join(frames),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )

    async def _sse_generator():
        async_q: "asyncio.Queue[Tuple[str, Any]]" = asyncio.Queue()

        def _on_stage(ev: Dict[str, Any]) -> None:
            running_loop.call_soon_threadsafe(async_q.put_nowait, ("stage", ev))

        def _worker() -> None:
            try:
                res = run_deterministic_charm_consultation(
                    payload,
                    entitlement_tier=entitlement,
                    on_stage=_on_stage,
                )
                running_loop.call_soon_threadsafe(async_q.put_nowait, ("result", res))
            except Exception as exc:
                running_loop.call_soon_threadsafe(async_q.put_nowait, ("error", exc))

        threading.Thread(target=_worker, daemon=True).start()

        while True:
            kind, item = await async_q.get()
            if kind == "stage":
                yield f"event: stage\ndata: {json.dumps(item, ensure_ascii=False)}\n\n"
            elif kind == "result":
                yield f"event: result\ndata: {json.dumps(item, ensure_ascii=False)}\n\n"
                break
            elif kind == "error":
                err_payload = {
                    "success": False,
                    "code": "CHARM_UNAVAILABLE",
                    "error": "Charm AI is unavailable right now, no credit was used. Try again.",
                    "credit_chargeable": False,
                }
                yield f"event: error\ndata: {json.dumps(err_payload, ensure_ascii=False)}\n\n"
                break

    resp = StreamingResponse(_sse_generator(), media_type="text/event-stream")
    resp.headers["Cache-Control"] = "no-cache"
    resp.headers["X-Accel-Buffering"] = "no"
    return resp
