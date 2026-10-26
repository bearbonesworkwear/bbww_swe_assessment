def test_latest_snapshot_wins(client):
    result=client.get('/api/inventory/BBW-004/BBW-BT-103').json()
    assert result['on_hand']==9, 'Should not use an older 22-unit snapshot'

def test_paid_unfulfilled_order_is_reserved_for_online_promise(client):
    # BBWW-2418: Rocklin: 9 on hand - 0 damaged - 2 active holds - 4 unfulfilled = 3
    result=client.get('/api/inventory/BBW-004/BBW-BT-103').json()
    assert result['web_commitments']==4
    assert result['available_to_promise']==3
