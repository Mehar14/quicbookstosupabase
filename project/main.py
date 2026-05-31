from database.supabase_client import get_supabase_client
from qbo.client import get_qbo_client
from sync.transfers import sync_customers_to_supabase


def main():
    qbo_client = get_qbo_client()
    supabase_client = get_supabase_client()

    

    sync_customers_to_supabase(qbo_client=qbo_client, supabase_client=supabase_client)

if __name__ == "__main__":
    main()