"""Operational view of failed/stale POS synchronizations."""
from datetime import datetime, timedelta

def pos_sync_exceptions(store, as_of='2026-10-26T08:30:00-07:00'):
    now = datetime.fromisoformat(as_of)
    exceptions = []
    for row in store.all('SELECT id, name, last_pos_sync_at FROM stores ORDER BY id'):
        lag_minutes = round((now-datetime.fromisoformat(row['last_pos_sync_at'])).total_seconds()/60)
        if lag_minutes > 120:
            exceptions.append({'severity':'critical' if lag_minutes > 240 else 'warning',
              'code':'POS_SYNC_STALE','store_id':row['id'],'store':row['name'],
              'lag_minutes':lag_minutes,'last_sync_at':row['last_pos_sync_at'],
              'message':f"POS import last succeeded {lag_minutes}m ago"})
    return exceptions
