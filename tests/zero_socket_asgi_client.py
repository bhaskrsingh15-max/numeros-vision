# -*- coding: utf-8 -*-
"""
tests/zero_socket_asgi_client.py
================================
Zero-socket synchronous ASGI 3.0 test client for FastAPI/Starlette apps.
Runs 100% without OS sockets (`socket.socketpair`), avoiding Windows sandbox loopback hangs.
"""

from __future__ import annotations

import json
import urllib.parse
from typing import Any, Dict, List, Optional, Tuple


class ZeroSocketResponse:
    def __init__(self, status_code: int, headers: Dict[str, str], body_bytes: bytes) -> None:
        self.status_code = status_code
        self.headers = headers
        self.content = body_bytes
        self.text = body_bytes.decode("utf-8", errors="replace")

    def json(self) -> Any:
        return json.loads(self.text)


def _drive_zero_socket_coro(coro):
    """Drives a pure/non-socket coroutine to completion."""
    val = None
    while True:
        try:
            yielded = coro.send(val)
            # If an async generator / sleep(0) yields None, continue driving
            val = yielded
        except StopIteration as exc:
            return exc.value


class ZeroSocketAsgiClient:
    def __init__(self, app: Any) -> None:
        self.app = app

    def request(
        self,
        method: str,
        url: str,
        *,
        json_body: Optional[Any] = None,
        raw_body: Optional[bytes] = None,
        headers: Optional[Dict[str, str]] = None,
        content_type: Optional[str] = None,
    ) -> ZeroSocketResponse:
        parsed = urllib.parse.urlsplit(url)
        path = parsed.path or "/"
        query_bytes = (parsed.query or "").encode("utf-8")

        if json_body is not None:
            body_bytes = json.dumps(json_body, ensure_ascii=False).encode("utf-8")
            ctype = content_type or "application/json"
        elif raw_body is not None:
            body_bytes = raw_body
            ctype = content_type or "application/octet-stream"
        else:
            body_bytes = b""
            ctype = content_type

        hdr_list: List[Tuple[bytes, bytes]] = [
            (b"host", b"testserver"),
            (b"content-length", str(len(body_bytes)).encode("ascii")),
        ]
        if ctype:
            hdr_list.append((b"content-type", ctype.encode("latin-1")))
        for k, v in (headers or {}).items():
            hdr_list.append((k.lower().encode("latin-1"), str(v).encode("latin-1")))

        scope = {
            "type": "http",
            "asgi": {"version": "3.0"},
            "http_version": "1.1",
            "method": method.upper(),
            "scheme": "http",
            "path": path,
            "raw_path": path.encode("utf-8"),
            "query_string": query_bytes,
            "headers": hdr_list,
            "client": ("127.0.0.1", 50000),
            "server": ("testserver", 80),
        }

        sent_request = False
        status_code = 500
        resp_headers: Dict[str, str] = {}
        chunks: List[bytes] = []

        async def receive() -> Dict[str, Any]:
            nonlocal sent_request
            if not sent_request:
                sent_request = True
                return {"type": "http.request", "body": body_bytes, "more_body": False}
            return {"type": "http.disconnect"}

        async def send(message: Dict[str, Any]) -> None:
            nonlocal status_code
            mtype = message.get("type")
            if mtype == "http.response.start":
                status_code = int(message.get("status", 200))
                for hk, hv in message.get("headers") or []:
                    resp_headers[hk.decode("latin-1").lower()] = hv.decode("latin-1")
            elif mtype == "http.response.body":
                b = message.get("body") or b""
                if b:
                    chunks.append(b)

        _drive_zero_socket_coro(self.app(scope, receive, send))
        return ZeroSocketResponse(status_code, resp_headers, b"".join(chunks))

    def get(self, url: str, *, headers: Optional[Dict[str, str]] = None) -> ZeroSocketResponse:
        return self.request("GET", url, headers=headers)

    def post(
        self,
        url: str,
        *,
        json: Optional[Any] = None,
        data: Optional[bytes] = None,
        headers: Optional[Dict[str, str]] = None,
        content_type: Optional[str] = None,
    ) -> ZeroSocketResponse:
        return self.request(
            "POST",
            url,
            json_body=json,
            raw_body=data,
            headers=headers,
            content_type=content_type,
        )
