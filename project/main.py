from database.schema import ensure_all_qbo_tables
from database.supabase_client import get_supabase_client, upsert_records
from qbo.client import get_qbo_client
from sync.runner import sync_all_entities


def main():
    qbo_client = get_qbo_client()
    supabase_client = get_supabase_client()

    ensure_all_qbo_tables(supabase_client=supabase_client)
    sync_all_entities(qbo_client, supabase_client, upsert_records)


if __name__ == "__main__":
    main()
