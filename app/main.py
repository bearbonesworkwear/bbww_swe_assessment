"""BareBones WorkWear Commerce Gateway — self-contained assessment fixture."""
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.config import settings
from app.storage import Store
from app.services.catalog import get_product, list_products
from app.services.inventory import availability, store_inventory
from app.services.ops import pos_sync_exceptions
from app.services.gear_assistant import recommend
from app.integrations.llm_provider import MockLLMProvider

class GearRequest(BaseModel):
    message: str = Field(min_length=3, max_length=500)
    store_id: str = 'BBW-004'
    max_price_usd: float | None = Field(default=None, gt=0)

def create_app(data_dir=None):
    from pathlib import Path
    data = Path(data_dir) if data_dir else settings.data_dir
    @asynccontextmanager
    async def lifespan(application):
        application.state.store = Store(data)
        application.state.llm = MockLLMProvider(data)
        yield
        application.state.store.close()

    app=FastAPI(title=settings.api_label, version='0.8.2', lifespan=lifespan)
    app.add_middleware(CORSMiddleware, allow_origins=settings.allow_origins,
        allow_methods=['GET','POST'], allow_headers=['Content-Type'])

    @app.get('/health')
    def health():
        return {'status':'ok','service':'commerce-gateway','fixture_mode':True,'version':'0.8.2'}

    @app.get('/api/stores')
    def stores(request: Request):
        return request.app.state.store.all('SELECT id,name,city,state,last_pos_sync_at FROM stores ORDER BY id')

    @app.get('/api/products')
    def products(request: Request,search: str='',category: str='',limit: int=Query(50,ge=1,le=100)):
        return {'items':list_products(request.app.state.store,search,category,limit)}

    @app.get('/api/products/{sku}')
    def product(request: Request,sku: str):
        item=get_product(request.app.state.store,sku)
        if not item: raise HTTPException(status_code=404,detail='Unknown SKU')
        return item

    @app.get('/api/inventory/{store_id}/{sku}')
    def inventory(request: Request,store_id: str,sku: str):
        result=availability(request.app.state.store,store_id,sku)
        if not result: raise HTTPException(status_code=404,detail='No product/store snapshot')
        return result

    @app.get('/api/inventory/{store_id}')
    def inventory_all(request: Request,store_id: str,limit: int=Query(40,ge=1,le=100)):
        if not request.app.state.store.one('SELECT id FROM stores WHERE id=?',(store_id,)):
            raise HTTPException(status_code=404,detail='Unknown store')
        return {'store_id':store_id,'items':store_inventory(request.app.state.store,store_id,limit)}

    @app.get('/api/ops/pos-sync-exceptions')
    def pos_exceptions(request: Request):
        return {'as_of':'2026-10-26T08:30:00-07:00',
          'exceptions':pos_sync_exceptions(request.app.state.store)}

    @app.post('/api/assistant/recommend')
    def gear_recommend(body: GearRequest,request: Request):
        if not request.app.state.store.one('SELECT id FROM stores WHERE id=?',(body.store_id,)):
            raise HTTPException(status_code=404,detail='Unknown store')
        return recommend(request.app.state.store,request.app.state.llm,body.message,body.store_id,body.max_price_usd)

    return app

app=create_app()
