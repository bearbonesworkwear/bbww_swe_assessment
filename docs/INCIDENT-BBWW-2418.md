# BBWW-2418 — Rocklin online ATP larger than real sellable stock

> MOCK INCIDENT · RETAIL SYSTEMS · OPEN · Severity P2 · As-of 2026-10-26, 08:30 PT

**Reported by:** store operations, Rocklin (BBW-004)  
**Affected flow:** POS snapshot → availability gateway → storefront promise  
**Customer impact (simulated):** A pickup order was accepted for a boot even though some of the rack stock was committed to existing paid, unfulfilled online orders.

## Reproduction reported by store manager
A Gear Advisor pilot shopper requests waterproof safety-toe boots for pickup at Rocklin. Operations sees the correct on-hand POS figure for SKU `BBW-BT-103`, but the online promise does not match the reservation and order queue. The employee confirms that cancelled orders should not hold stock and that completed web shipments have already been reflected in the latest POS count.

## Acceptance criteria
- Inventory promise is based on the **newest** POS count, minus damaged, active store holds and paid/unfulfilled e-commerce commitments.
- Cancelled/refunded/fulfilled order lines do not reserve stock.
- Never return negative ATP.
- No SKU-specific special-cases; test more than the reported item if you can.

## Why this matters
The same availability signal is planned for the website, marketplaces, and AI product recommendations. One bug at this seam propagates to all channels.

## Boundaries
The assessment data includes event-like rows but is **not** a full inventory ledger. Don't rebuild the entire event-sourcing model inside the interview. Explain any assumptions you would confirm with POS engineering in production.
