# BareBones WorkWear · Commerce Integration Gateway

**Internal prototype · Commerce Platform / Retail Systems · Release 2026.10-RC2**

BareBones WorkWear operates 10 stores in Northern California alongside an online storefront and B2B uniform programs. This repository models the internal service that makes online product promises match store reality: POS stock counts, held items, unfulfilled e-commerce orders, supplier ETAs and a planned AI Gear Advisor.

**Engineering candidate? Start with [ASSESSMENT.md](ASSESSMENT.md).**

> **IMPORTANT — simulated environment.** All data, orders, incident tickets, supplier records, integration feeds and source code are synthetic assessment fixtures. This repository is not a real internal system and contains no production credentials, real customers, actual orders, or proprietary operational data.

## Why this exists

Store managers are good at selling the right gear. Online shoppers don't always know whether a boot is waterproof or what size a crew needs. Meanwhile, a stock figure from POS is not necessarily sellable inventory: some units are reserved for pickup, others are already committed to web orders. We need one trustworthy availability projection behind the storefront, marketplace feed and a future AI product assistant.

Current simulated operational issues:
- **BBWW-2418** — Rocklin store web availability may promise units already reserved by online orders.
- **BBWW-2460** — Gear Advisor frontend exists, but recommendation service is not catalog-grounded yet.
- **BBWW-2482** — Placerville POS feed was stale during the morning monitor run.

## System map

```text
  POS exports (10 stores)   E-commerce order lines    Supplier SFTP feed
           \                    |                   /
            \                   |                  /
          [SQLite fixture loader / ingestion boundary]
                               |
                      FastAPI commerce gateway
                      /          |            \
              /api/inventory  /api/products  /api/assistant/recommend
                       |                       ^
                       |                 Mock LLM provider
                       |                  (UNTRUSTED)
                       +--------------+--------+
                                      |
                              Next.js workbench
                            /ops + /gear-guide
```

## Repository layout

```text
app/                         Python/FastAPI gateway
  main.py                     Routes and app lifecycle
  storage.py                  SQLite tables and seed import
  services/inventory.py       Available-to-promise calculation
  services/catalog.py         Catalog lookup / SQL filters
  services/gear_assistant.py  LLM-grounding integration point
  integrations/llm_provider.py Offline provider with imperfect suggestions
web/app/                      Next.js 15 operations UI + Gear Advisor
data/                         Entirely synthetic feed fixtures
docs/                         Incident, integrations, design and API notes
tests/                        Public pytest tests (one starts red)
.github/workflows/ci.yml     CI starter
ASSESSMENT.md                 Candidate task instructions
NOTES.md                      Candidate decision log
```

## Run locally

Requires **Python 3.11+**. No API keys, cloud account or database server needed.

```bash
python -m venv .venv
source .venv/bin/activate               # Windows: .venv\Scripts\activate
python -m pip install -r requirements-dev.txt
make run                                # or: uvicorn app.main:app --reload
# http://127.0.0.1:8000/docs
```

In a second terminal:
```bash
make test      # expected baseline: one failing inventory test; one skipped assistant test
```

Optional Next.js interface (**Node 20+**; npm install may require internet):
```bash
cd web
cp .env.example .env.local
npm install
npm run dev    # http://localhost:3000
```

If Node isn't installed or packages cannot be downloaded, **do the backend tasks first**. UI is not required to complete the core assessment.

## Quick API checks

```bash
curl http://127.0.0.1:8000/health
curl 'http://127.0.0.1:8000/api/inventory/BBW-004/BBW-BT-103'
curl 'http://127.0.0.1:8000/api/ops/pos-sync-exceptions'
curl -X POST 'http://127.0.0.1:8000/api/assistant/recommend' -H 'Content-Type: application/json' -d '{"message":"waterproof safety toe boots under $160","store_id":"BBW-004","max_price_usd":160}'
```

## Engineering notes

This snapshot is intentionally *unfinished*, not a treasure hunt for obscure syntax. It contains a real business logic defect, an incomplete integration seam and visible operational tradeoffs. Prefer small, tested changes and a clear explanation of what you would ship next.

[Architecture](docs/ARCHITECTURE.md) · [Incident](docs/INCIDENT-BBWW-2418.md) · [Gear Advisor brief](docs/PRODUCT-BRIEF.md) · [API reference](docs/API.md) · [Data dictionary](data/README.md)
