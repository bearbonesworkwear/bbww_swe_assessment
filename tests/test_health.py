def test_health(client):
    data=client.get('/health').json()
    assert data['status']=='ok'
    assert data['fixture_mode'] is True

def test_stores_are_realistic_mock_locations(client):
    stores=client.get('/api/stores').json()
    assert len(stores)==10
    assert {s['id'] for s in stores} == {f'BBW-{i:03d}' for i in range(1,11)}

def test_unknown_inventory_returns_404(client):
    assert client.get('/api/inventory/BBW-004/UNKNOWN').status_code == 404
