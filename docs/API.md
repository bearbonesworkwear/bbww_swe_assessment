# API quick reference
FastAPI docs: `/docs` when running the gateway on port 8000.

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/health` | status + fixture flag |
| GET | `/api/stores` | list configured store locations |
| GET | `/api/products?search=&category=&limit=` | merch catalog lookup |
| GET | `/api/products/{sku}` | details and tags |
| GET | `/api/inventory/{store_id}/{sku}` | computed availability-to-promise |
| GET | `/api/inventory/{store_id}?limit=40` | store availability list |
| GET | `/api/ops/pos-sync-exceptions` | stale POS monitoring |
| POST | `/api/assistant/recommend` | model-assisted recommendations (501 at baseline) |

Example assistant body:
```json
{"message":"waterproof safety-toe boots for under $160","store_id":"BBW-004","max_price_usd":160}
```

The implementation intentionally returns `501 Not Implemented` for the assistant on the starting branch. See `ASSESSMENT.md` for the response contract.
