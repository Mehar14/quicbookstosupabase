from supabase import create_client, Client

from config import SUPABASE_URL, SUPABASE_KEY


def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def upsert_records(
    supabase_client: Client,
    table: str,
    records: list[dict],
    on_conflict: str = "qbo_id",
) -> None:
    if not records:
        return

    supabase_client.table(table) \
        .upsert(records, on_conflict=on_conflict) \
        .execute()
