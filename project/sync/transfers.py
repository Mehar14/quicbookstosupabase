from quickbooks.customers import fetch_customers


def transform_customers(qbo_client):
    customers = fetch_customers(qbo_client)

    records = []

    for c in customers:
        records.append({
            "qbo_id": c.Id,
            "display_name": c.DisplayName,
            "email": (
                getattr(c.PrimaryEmailAddr, "Address", None)
                if c.PrimaryEmailAddr
                else None
            ),
            "company_name": c.CompanyName,
            "balance": float(c.Balance or 0),
        })

    return records


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