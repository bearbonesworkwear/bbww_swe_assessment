# Architecture overview — assessment-only projection

## Integration boundaries
Retail POS exports latest `on_hand` (includes damaged units, excludes previously shipped merchandise). Store pickup team maintains active holds. Website and marketplace order lines can be paid/unfulfilled, fulfilled, cancelled or refunded. The projection determines the quantity that may be promised to another buyer. Supplier inbound ETAs do not increase ATP.

The adapter `app/storage.py` loads each mock feed into SQLite `:memory:` at app startup. Production systems would ingest incrementally with schema validation, idempotency, supplier-store reconciliation, logging and durable persistence. This exercise intentionally omits network integrations to remain deterministic.

## Service boundaries
- HTTP layer: `app/main.py` validates request types and store IDs.
- Data projection: `app/services/inventory.py` determines ATP from latest POS/holds/order states.
- Catalog: `app/services/catalog.py` provides verified merch attributes (price is authoritative here).
- AI boundary: `app/integrations/llm_provider.py` simulates a provider; `app/services/gear_assistant.py` must enforce trust boundaries.
- Web: Next.js 15 app-router screens in `web/app/`. `NEXT_PUBLIC_GATEWAY_URL` points to FastAPI.
- Observability: stale POS import view in `app/services/ops.py`.

## Known limitations
No authentication, per-store authorization, accounting writeback, payments, durable reservation locks, human safety-compliance review, high-load concurrency or live supplier synchronization. Do not deploy. The current app is read-only except for a simulated suggestion endpoint.

## Production discussion (not an assessment requirement)
We would likely provision managed Postgres + event ingestion + idempotent order updates; store-aware cache TTL; traceable data provenance; non-root containers; CI with tests, type checks and frontend build; protected secrets/roles; alerts for stale feeds and inventory promise drift. Candidate may prioritize a subset.
