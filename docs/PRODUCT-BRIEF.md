# BBWW-2460 — Gear Advisor: catalog-grounded prototype

> MOCK PRODUCT BRIEF · E-COMMERCE + MERCHANDISING · Pilot target: Q4 2026

## User story
As a working tradesperson, I want to describe what I need (e.g. waterproof safety-toe boots under $160) and see real, in-stock products available for pickup at my chosen store.

**Why it matters:** A generic chatbot could invent a product, claim a boot has a safety certification not recorded in our catalog, or direct customers to a store with zero stock. A useful product advisor must be grounded in our own product records and inventory promise.

## Stage 1 contract
- Request: `POST /api/assistant/recommend`, body `message` (3–500 chars), `store_id`, optional `max_price_usd`.
- The offline provider returns a shortlist of SKU identifiers. Some are invalid, unavailable or out of budget.
- Verify each against active catalog records and current-store ATP.
- Emit at most 3 items with SKU, brand, name, current mock price, ATP, and a short reason supported by tags and/or stock.
- Never rely on provider prose for price, physical stock or safety claims; never expose keys or raw internal supplier cost to shoppers.
- For no matches, return empty array rather than hallucinating alternatives.

## Stage 2 / not in interview scope
- Real LLM API client with timeout/retries, JSON schema outputs and spend budgets.
- User-intent extraction with retrieval-grounding and review for safety specifications.
- Feature flags, analytics and rollout to limited stores, accessibility and localization.
- Proper stock freshness/latency guarantees, hold placement at checkout.

## Definition of done for mock
Local endpoint returns a schema suitable for the existing Next.js frontend, no credentials or network call required, with tests for known invalid/OOS suggestions.
