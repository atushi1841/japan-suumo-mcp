# Suumo Japan Real Estate Price Stats API MCP Server

MCP server wrapping the Suumo Japan Real Estate Price Stats API (RapidAPI FREEMIUM).

## Tools

- `get_api_info()` — metadata and RapidAPI URL
- `query_api(params)` — proxy call to RapidAPI endpoint (requires RAPIDAPI_KEY)

## Links

- **RapidAPI**: https://rapidapi.com/atsushi-noriduki/api/suumo-japan-real-estate-price-stats-api
- **Apify Store**: https://apify.com/fruitful_quintessence
- **GitHub**: https://github.com/atushi1841/japan-suumo-mcp
- **Smithery**: https://smithery.ai/server/atushi1841/japan-suumo-mcp

## Install (Smithery)

```bash
smithery install @atushi1841/japan-suumo-mcp
```

## Run locally

```bash
pip install fastmcp
python server.py          # stdio MCP transport
python server.py --http   # streamable-http at /mcp
```

## Environment

- `RAPIDAPI_KEY` (optional): free key from https://rapidapi.com/atsushi-noriduki/api/suumo-japan-real-estate-price-stats-api
