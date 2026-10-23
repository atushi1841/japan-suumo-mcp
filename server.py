#!/usr/bin/env python3
"""japan-suumo-mcp: MCP server wrapping the RapidAPI Japan-Suumo API.

Exposes tools:
  - get_api_info(): metadata and RapidAPI URL for the Japan-Suumo service.
  - query_api(params): proxy call to the underlying RapidAPI endpoint (requires RAPIDAPI_KEY env).

Data source: https://rapidapi.com/atsushi-noriduki/api/japan-suumo
Apify Store: https://apify.com/fruitful_quintessence
GitHub: https://github.com/atushi1841/japan-suumo-mcp
"""
from __future__ import annotations

import os
import sys
import urllib.request
import urllib.parse
from typing import Any, Dict, Optional

from fastmcp import FastMCP

mcp = FastMCP("japan-suumo-mcp")

RAPIDAPI_SLUG = "japan-suumo"
RAPIDAPI_HOST = f"{RAPIDAPI_SLUG}.rapidapi.com"
RAPIDAPI_BASE = f"https://{RAPIDAPI_HOST}"
RAPIDAPI_URL = f"https://rapidapi.com/atsushi-noriduki/api/{RAPIDAPI_SLUG}"

DESCRIPTION = """Suumo Japan Real Estate Price Stats API（SUUMO 不動産価格統計API）
SUUMO 掲載物件の価格推移・種別・地域別統計を取得。AIエージェントの不動産調査に。"""


@mcp.tool()
def get_api_info() -> Dict[str, Any]:
    """Return metadata, RapidAPI URL, and usage notes for the Japan-Suumo data source.

    Use this tool to get the API endpoint URL, pricing tier, and integration notes.
    Returns structured JSON with api_name, slug, rapidapi_url, pricing, description.
    """
    return {
        "api_name": "Japan-Suumo",
        "slug": RAPIDAPI_SLUG,
        "rapidapi_host": RAPIDAPI_HOST,
        "rapidapi_url": RAPIDAPI_URL,
        "pricing": "FREEMIUM",
        "description": DESCRIPTION,
        "requirements": [
            "RAPIDAPI_KEY env var (free, get at https://rapidapi.com/atsushi-noriduki)",
            "Call via https://{RAPIDAPI_HOST}/...",
        ],
        "related": {
            "apify_store": "https://apify.com/fruitful_quintessence",
            "github_repo": f"https://github.com/atushi1841/japan-suumo-mcp",
            "smithery": f"https://smithery.ai/server/atushi1841/japan-suumo-mcp",
        },
    }


@mcp.tool()
def query_api(params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Call the Japan-Suumo RapidAPI endpoint and return the response.

    Requires RAPIDAPI_KEY environment variable (free key from RapidAPI).
    If key is missing, returns instructions for obtaining one.

    Args:
        params: Optional query parameters specific to this API. Defaults to empty dict.

    Returns:
        Response JSON from the RapidAPI endpoint, or an error/instruction message.
    """
    key = os.environ.get("RAPIDAPI_KEY", "").strip()
    if not key:
        return {
            "error": "RAPIDAPI_KEY not set",
            "instructions": [
                "1. Go to {RAPIDAPI_URL}",
                "2. Sign up for free (if needed)",
                "3. Copy your API key from the RapidAPI dashboard",
                "4. Set: export RAPIDAPI_KEY=<your_key>",
            ],
            "rapidapi_url": RAPIDAPI_URL,
        }
    try:
        url = f"{RAPIDAPI_BASE}/"
        qp = urllib.parse.urlencode(params or {})
        if qp:
            url = url + "?" + qp
        req = urllib.request.Request(
            url,
            headers={
                "X-RapidAPI-Key": key,
                "X-RapidAPI-Host": RAPIDAPI_HOST,
            },
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read().decode()
            return {
                "status": resp.status,
                "data": data[:5000],
                "note": "Response truncated to 5000 chars; full response available in logs",
            }
    except Exception as e:
        return {
            "error": str(e),
            "hint": "Check RAPIDAPI_KEY validity and endpoint availability.",
            "rapidapi_url": RAPIDAPI_URL,
        }


if __name__ == "__main__":
    transport = sys.argv[1] if len(sys.argv) > 1 else "stdio"
    mcp.run(transport=transport)
