def test_stale_pos_sync_is_exposed(client):
    result=client.get('/api/ops/pos-sync-exceptions').json()
    assert any(e['store_id']=='BBW-010' and e['code']=='POS_SYNC_STALE' for e in result['exceptions'])
