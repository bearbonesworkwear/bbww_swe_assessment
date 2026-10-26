"""Local fixture-backed SQLite adapter. Real integrations are represented by synthetic exports."""
import csv
import json
import sqlite3
from pathlib import Path

def _read_jsonl(path: Path):
    with path.open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]

class Store:
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._load()

    def _load(self):
        self.conn.executescript("""
        CREATE TABLE catalog (sku TEXT PRIMARY KEY, brand TEXT, name TEXT, category TEXT,
          price_usd REAL, tags TEXT, size TEXT, color TEXT, is_active INTEGER);
        CREATE TABLE stores (id TEXT PRIMARY KEY, name TEXT, city TEXT, state TEXT,
          channel TEXT, last_pos_sync_at TEXT);
        CREATE TABLE pos_snapshots (snapshot_id TEXT PRIMARY KEY, store_id TEXT, sku TEXT,
          on_hand INTEGER, damaged INTEGER, captured_at TEXT, batch_id TEXT);
        CREATE TABLE store_holds (hold_id TEXT PRIMARY KEY, store_id TEXT, sku TEXT,
          qty INTEGER, status TEXT, reason TEXT, expires_at TEXT);
        CREATE TABLE order_lines (event_id TEXT PRIMARY KEY, order_id TEXT, line_id TEXT,
          store_id TEXT, sku TEXT, qty INTEGER, status TEXT, fulfillment_status TEXT,
          channel TEXT, created_at TEXT);
        CREATE TABLE supplier_inbound (vendor_sku TEXT PRIMARY KEY, sku TEXT,
          vendor_name TEXT, eta_date TEXT, qty_inbound INTEGER, cost_usd REAL);
        CREATE INDEX idx_pos_store_sku_date ON pos_snapshots (store_id,sku,captured_at DESC);
        CREATE INDEX idx_order_store_sku ON order_lines (store_id,sku);
        """)
        def insert(table, keys, row):
            cols = ','.join(keys)
            placeholders = ','.join('?' for _ in keys)
            self.conn.execute(f"INSERT INTO {table} ({cols}) VALUES ({placeholders})", [row.get(k) for k in keys])

        for p in json.loads((self.data_dir/'catalog.json').read_text()):
            p['tags'] = json.dumps(p['tags'])
            p['is_active'] = int(p['is_active'])
            insert('catalog', ['sku','brand','name','category','price_usd','tags','size','color','is_active'],p)
        for p in json.loads((self.data_dir/'stores.json').read_text()):
            insert('stores',['id','name','city','state','channel','last_pos_sync_at'],p)
        with (self.data_dir/'pos_inventory_snapshots.csv').open(newline='') as file:
            for p in csv.DictReader(file):
                insert('pos_snapshots',['snapshot_id','store_id','sku','on_hand','damaged','captured_at','batch_id'],p)
        for p in json.loads((self.data_dir/'store_holds.json').read_text()):
            insert('store_holds',['hold_id','store_id','sku','qty','status','reason','expires_at'],p)
        for p in _read_jsonl(self.data_dir/'web_order_lines.jsonl'):
            insert('order_lines',['event_id','order_id','line_id','store_id','sku','qty','status','fulfillment_status','channel','created_at'],p)
        with (self.data_dir/'supplier_inbound.csv').open(newline='') as file:
            for p in csv.DictReader(file):
                insert('supplier_inbound',['vendor_sku','sku','vendor_name','eta_date','qty_inbound','cost_usd'],p)
        self.conn.commit()

    def all(self, sql: str, params: tuple=()):
        return [dict(r) for r in self.conn.execute(sql, params).fetchall()]

    def one(self, sql: str, params: tuple=()):
        row = self.conn.execute(sql, params).fetchone()
        return dict(row) if row else None

    def close(self):
        self.conn.close()
