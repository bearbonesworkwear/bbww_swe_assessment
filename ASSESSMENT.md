# Software Engineer — Live Coding Assessment
**BareBones WorkWear · Commerce & AI Integrations**

Thank you for meeting with us. You're joining an imagined snapshot of an existing internal project: a small commerce gateway between 10 retail stores, an e-commerce channel and a future AI-powered product advisor.

**Timebox:** 60 minutes of coding and discussion during your HR intro call (up to 75 minutes including setup and wrap-up). We do not expect a production-complete solution. A prioritized, reviewed change is better than rushing through every item.

## How to work
- **Use Cursor.** Cursor Chat, inline edit, and **Agent mode are all welcome**. We want to see how you scope tasks for coding agents, inspect their proposed edits, validate outputs, and recover when suggestions are wrong.
- Narrate key decisions as you work, especially prompts, test results, AI mistakes, and tradeoffs. A screen recording (no webcam required) and your code change will be sent to our engineering reviewer after your call.
- You may search documentation. You do **not** need paid LLM credits, cloud accounts, real company credentials, Docker, or an API key. The LLM fixture is offline on purpose.
- Do not paste personal, private, or third-party secrets into the fixture or Cursor chat. This is entirely simulated data.

## Before you start (~5 min)
1. Skim `README.md`, `docs/INCIDENT-BBWW-2418.md`, `docs/PRODUCT-BRIEF.md`.
2. Run `make test` (or `python -m pytest -q`) and inspect the failing test.
3. Open the code in Cursor and decide what you will do first.

## Your work (~50 min)

### Task A — Fix the inventory promise incident (priority 1, ~15–20 min)
Store associates reported a mismatch between POS stock on hand and the number of units promised to online customers. One public test fails in a clean checkout. **Find and fix the underlying cause, without hard-coding a SKU or changing the failing assertion.**

Expected domain rules, for this snapshot:
- Latest POS snapshot for a store/SKU is the physical source of truth.
- Damaged stock and `active` in-store holds are not sellable.
- **Paid + unfulfilled** web order lines reserve stock; fulfilled, cancelled and refunded lines must not reserve stock again.
- ATP should never be negative. Return the reserved web quantity in `web_commitments`.
- Avoid relying on a hard-coded fixture date to make the calculation work.

Demonstrate the corrected API or test output. Add or improve at least one meaningful edge-case test if time allows.

### Task B — Implement a catalog-grounded AI Gear Advisor (priority 2, ~20–25 min)
The storefront at `web/app/gear-guide/page.tsx` calls `POST /api/assistant/recommend`. The route and offline model adapter are already present, but the service in `app/services/gear_assistant.py` currently responds `501`.

Implement a small useful first version. Provider suggestions are **untrusted**: the fixture deliberately suggests non-existent SKUs and products that may be out of stock or above budget.

Required response shape:
```json
{
  "query": "waterproof safety toe boots under $160",
  "store_id": "BBW-004",
  "recommendations": [
    {
      "sku": "BBW-BT-103",
      "brand": "Wolverine",
      "name": "ForcePoint Waterproof Composite Toe",
      "price_usd": 149.95,
      "available_to_promise": 3,
      "reason": "Waterproof composite-toe boot; 3 available at Rocklin."
    }
  ],
  "disclaimer": "Availability is a point-in-time estimate; verify before checkout."
}
```
- Only return **active catalog products** that the fixture provider suggested and that exist in the catalog.
- Only return products **with ATP > 0 at the requested store**.
- Respect optional `max_price_usd`, return **at most 3** products, and do not mutate prices/SKUs based on LLM prose.
- Use **catalog attributes and computed availability** to justify each result; no invented technical specifications or promises.
- Reasonable behavior for no matches is an empty recommendations array. Keep the API safe for bad/unknown store IDs (the route handles unknown locations).
- You do **not** have to call an actual LLM API. The offline adapter exists so you can demonstrate **safe LLM integration and verification** without credentials or external dependence.

You may unskip and expand `tests/test_assistant_contract.py` when you've implemented the contract.

### Task C — Show ownership (priority 3, ~10–15 min)
Choose **one** improvement that matters for deploying or maintaining a system like this. Examples: a CI gate covering frontend build or lint, a meaningful test covering cancellation/fulfillment behavior, observability for the inventory feed, a robust stale-inventory policy, or a user-visible Gear Advisor failure state. Explain what you chose and what remains risky.

Don't attempt all these examples. We want to see prioritization across backend, frontend, data and operations.

## Deliverables (end of call)
1. Your changes as a Git diff/patch or repository ZIP (do not include `.venv`, `node_modules`, or secrets).
2. Your **screen recording of Cursor use and terminal/tests**, with narration if possible.
3. A short `NOTES.md`: what changed, what your AI assistant did, what you accepted/rejected, tests run, limitations and what you'd do with another day.

## What we evaluate

| We care about | Not required |
| --- | --- |
| Correct business rules & sensible tests | Finishing every stretch task |
| Critical use of AI coding agents | Typing without AI |
| Catalog grounding and safe LLM boundaries | A paid AI API key |
| Clear full-stack/integration decisions | Rewriting our demo UI |
| Ownership, tradeoffs & concise communication | Production deployment in an hour |

## Data / privacy
All company scenarios and identifiers are fictional hiring fixtures created to resemble retail integrations. You are not handling real customers or internal company credentials. You can decline recording and discuss an alternate live review with the recruiter.
