from qbo.customers import fetch_customers


def transform_customers(qbo_client):
    customers = fetch_customers(qbo_client)

    
    print(customers[0].to_dict())

    return customers


def sync_customers_to_supabase(
    qbo_client,
    supabase_client
):
    records = transform_customers(qbo_client)

    if not records:
        return

    supabase_client.table("qbo_customers") \
        .upsert(records, on_conflict="qbo_id") \
        .execute()

    print(f"Synced {len(records)} customers")