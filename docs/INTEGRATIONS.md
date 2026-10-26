# Integration contracts (synthetic)

**POS to gateway:** Each `pos_inventory_snapshots.csv` record is store/SKU point-in-time physical count. `captured_at` may differ between stores. The loader retains history; use newest captured_at for each pair. Damaged units are unavailable.

**Web commerce to gateway:** `web_order_lines.jsonl` is a normalized event export, one current-status row per mock order line in this fixture. Only `status=paid` AND `fulfillment_status=unfulfilled` reduces currently sellable physical stock. A shipped order is already reflected in POS; double subtraction causes false stock-outs.

**Store pickup:** `store_holds.json` states whether an in-store pickup hold is still active. Ignore released/expired holds. A production system would need TTL, reservation replays, and race-condition protection.

**Supplier to Merchandising:** `supplier_inbound.csv` provides upcoming replenishments and unit cost for internal replenishment planning. Costs must not be returned through public web routes.

**Gear Advisor:** Model-like suggestions in `mock_llm_responses.json` are untrusted candidates; may reference fictional SKUs. Product specs, price, and ATP must come from our own data, not provider text.

**Out of scope:** Real POS vendor choice and endpoints, accounting service credentials, real marketplace publication, actual logistics API, PCI and payment processing.
