"""Product master lookup. Search is intentionally a modest prototype."""
import json

def list_products(store, search: str='', category: str='', limit=50):
    q = 'SELECT sku,brand,name,category,price_usd,tags,size,color FROM catalog WHERE is_active=1'
    params = []
    if search:
        q += ' AND (LOWER(name) LIKE ? OR LOWER(brand) LIKE ? OR LOWER(tags) LIKE ?)'
        term = '%' + search.lower() + '%'
        params.extend([term, term, term])
    if category:
        q += ' AND category=?'
        params.append(category)
    q += ' ORDER BY category, brand, sku LIMIT ?'
    params.append(limit)
    rows = store.all(q,tuple(params))
    for row in rows:
        row['tags'] = json.loads(row['tags'])
    return rows

def get_product(store, sku: str):
    row = store.one('SELECT sku,brand,name,category,price_usd,tags,size,color,is_active FROM catalog WHERE sku=?',(sku,))
    if row:
        row['tags']=json.loads(row['tags'])
    return row
