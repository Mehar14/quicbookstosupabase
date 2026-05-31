from supabase import create_client, Client

from config import SUPABASE_URL, SUPABASE_KEY


def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def upsert_qbo_customers(supabase_client: Client, records: list[dict]) -> None:
    if not records:
        return

    supabase_client.table("qbo_customers") \
        .upsert(records, on_conflict="qbo_id") \
        .execute()
