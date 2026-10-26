# Commerce Systems on-call notes (mock)

| Signal | Action |
| --- | --- |
| `POS_SYNC_STALE` >120 min | Stop or downgrade web inventory promise for affected store until backfill succeeds. |
| ATP < 0 | Should be capped at 0; inspect reservations and POS lag. |
| Gear Advisor unknown SKU | Reject model suggestion, log a structured rejection reason (never invent product). |
| Upstream provider unavailable | Fail closed with empty recommendation set or user-friendly retry; don't guess stock. |

Simulated RC2 owner: Retail Systems. Rollback plan (conceptual): disable pilot Gear Advisor flag; continue trusted catalog browsing. Release evidence would be test logs, container scan, front-end build and a safe smoke check against staging mocks.
