from database.schema import ensure_all_qbo_tables
from database.supabase_client import get_supabase_client, upsert_records
from qbo.client import get_qbo_client
from sync.registry import ENTITY_SYNC_CONFIGS
from sync.registry import ENTITY_SYNC_CONFIGS


def run_full_sync() -> list[dict]:
    qbo_client = get_qbo_client()
    supabase_client = get_supabase_client()

    ensure_all_qbo_tables(supabase_client=supabase_client)

    results = []
    for config in ENTITY_SYNC_CONFIGS:
        try:
            items = config.fetch(qbo_client)
            records = [config.transform(item) for item in items]
            if records:
                upsert_records(
                    supabase_client,
                    config.table,
                    records,
                    config.conflict_column,
                )
            results.append({
                "name": config.name,
                "table": config.table,
                "count": len(records),
                "status": "ok",
            })
        except Exception as error:
            results.append({
                "name": config.name,
                "table": config.table,
                "count": 0,
                "status": "error",
                "error": str(error),
            })

    return results
