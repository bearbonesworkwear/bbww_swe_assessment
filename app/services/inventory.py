"""Fulfillment availability (ATP) projection consumed by web and operations."""
from datetime import datetime

def latest_pos(store, store_id: str, sku: str):
    return store.one("""
      SELECT store_id, sku, on_hand, damaged, captured_at, batch_id
      FROM pos_snapshots WHERE store_id=? AND sku=?
      ORDER BY captured_at DESC LIMIT 1
    """, (store_id, sku))

def availability(store, store_id: str, sku: str):
    item = store.one("SELECT sku, name, is_active FROM catalog WHERE sku=?", (sku,))
    location = store.one("SELECT id, name, last_pos_sync_at FROM stores WHERE id=?", (store_id,))
    if not item or not location:
        return None
    latest = latest_pos(store, store_id, sku)
    if latest is None:
        return None
    holds = store.one("""SELECT COALESCE(SUM(qty),0) AS qty FROM store_holds
        WHERE store_id=? AND sku=? AND status='active'
    """, (store_id, sku))['qty']

    # TODO BBWW-2418: ecommerce reservations are not being applied correctly.
    # The fulfillment team believes web reservations should affect the online promise.
    online = store.one("""SELECT COALESCE(SUM(qty),0) AS qty FROM order_lines
        WHERE store_id=? AND sku=? AND status='paid' AND fulfillment_status='fulfilled'
    """, (store_id, sku))['qty']
    physical = max(0, int(latest['on_hand']) - int(latest['damaged']))
    atp = max(0, physical - holds - online)
    return {'sku': sku, 'store_id': store_id, 'product': item['name'],
            'on_hand': int(latest['on_hand']), 'damaged': int(latest['damaged']),
            'active_store_holds': holds, 'web_commitments': online, 'available_to_promise': atp,
            'snapshot_at': latest['captured_at'], 'source_batch': latest['batch_id']}

def store_inventory(store, store_id: str, limit=60):
    rows = store.all("SELECT sku FROM catalog WHERE is_active=1 ORDER BY sku LIMIT ?", (limit,))
    return [availability(store, store_id, row['sku']) for row in rows]
