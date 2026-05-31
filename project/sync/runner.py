from sync.registry import ENTITY_SYNC_CONFIGS


def sync_entity(qbo_client, supabase_client, config, upsert_records) -> None:
    items = config.fetch(qbo_client)
    records = [config.transform(item) for item in items]

    if not records:
        print(f"No {config.name} to sync")
        return

    upsert_records(supabase_client, config.table, records, config.conflict_column)
    print(f"Synced {len(records)} {config.name}")


def sync_all_entities(qbo_client, supabase_client, upsert_records) -> None:
    for config in ENTITY_SYNC_CONFIGS:
        sync_entity(qbo_client, supabase_client, config, upsert_records)
