import pytest

@pytest.mark.skip(reason='BBWW-2460 deliberately unimplemented; see ASSESSMENT.md')
def test_advisor_never_returns_fictional_skus(client):
    response=client.post('/api/assistant/recommend',json={
        'message':'waterproof safety-toe boots for a construction job',
        'store_id':'BBW-004','max_price_usd':160})
    assert response.status_code==200
    body=response.json()
    assert body['recommendations']
    assert all(r['sku']!='FAKE-BT-999' for r in body['recommendations'])
