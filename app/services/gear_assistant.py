"""Catalog-grounded recommendation adapter (BBWW-2460 work-in-progress).

Suggested SKUs from the model are *not* facts. An LLM can invent products,
recommend an unsafe item, or cite stale pricing/stock. The application must
validate suggestions before anything appears on the storefront.
"""
from fastapi import HTTPException

def recommend(store, provider, message: str, store_id: str, max_price_usd: float | None):
    # Work item BBWW-2460: wire provider to live catalog and inventory projection.
    # See docs/PRODUCT-BRIEF.md and ASSESSMENT.md for the contract.
    raise HTTPException(status_code=501, detail='Catalog-grounded gear advisor is not implemented yet')
