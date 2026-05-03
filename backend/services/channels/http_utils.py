from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any


def post_json(url: str, payload: dict[str, Any], headers: dict[str, str] | None = None) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", **(headers or {})},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return {"ok": 200 <= response.status < 300, "status_code": response.status}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "status_code": exc.code, "error": str(exc)}
    except Exception as exc:
        return {"ok": False, "status_code": None, "error": str(exc)}
