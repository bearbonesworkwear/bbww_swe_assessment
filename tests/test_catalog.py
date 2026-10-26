def test_search_filter(client):
    result=client.get('/api/products',params={'search':'work boot'}).json()['items']
    assert result
    assert all('boot' in p['name'].lower() or 'boot' in p['tags'] for p in result)

def test_products_have_consistent_currency_prices(client):
    result=client.get('/api/products',params={'limit':100}).json()['items']
    assert len(result)>=30
    assert all(p['price_usd'] > 0 for p in result)
