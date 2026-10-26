# Data dictionary — simulated operational exports

**ALL RECORDS IN THIS FOLDER ARE SYNTHETIC.** Store locations are based on publicly listed BBWW cities, but store IDs, product SKUs, brands' mock product configurations, prices, counts, customers, timestamps, POS events, and supplier records are fabricated. They do not indicate real BBWW sales or inventory.

| File | Source label | Simulated cadence | Key fields |
| --- | --- | --- | --- |
| `stores.json` | Retail Systems registry | daily | store id, last POS sync |
| `catalog.json` | Merch PIM v2 | nightly | SKU, attributes, tags, list price |
| `pos_inventory_snapshots.csv` | Retail POS v3 export | 30–60 min | store, SKU, on-hand, damaged, captured_at |
| `store_holds.json` | Store pickup queue | event-driven | holds with active / released / expired status |
| `web_order_lines.jsonl` | Website and marketplace events | near-real-time | order status, fulfillment status, quantities |
| `supplier_inbound.csv` | Vendor inbound feed / SFTP | once daily | vendor mapping, inbound ETA, costs |
| `mock_llm_responses.json` | Gear Advisor provider simulation | on request | recommended SKUs (untrusted) |
| `metadata.json` | Integration fixture manifest | per assessment | snapshot time and provenance |

Known fixture examples (not answers to every test):
- `BBW-004` = Rocklin. `BBW-010` = Placerville, intentionally stale sync as a monitoring example.
- `BBW-BT-103` = a waterproof safety-toe boot. Rocklin has two active/retired pickup records, one fulfilled/cancelled ordering scenario and an unfulfilled web commitment.
- `FAKE-BT-999` is intentionally suggested by an untrusted mock provider but is NOT a real catalog SKU.

Do not assume every feed is clean, all timestamps are fresh, or a supplier inbound quantity means on-hand stock.
