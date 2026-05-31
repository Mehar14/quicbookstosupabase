CREATE TABLE IF NOT EXISTS public.qbo_tax_agencies (
    qbo_id TEXT PRIMARY KEY,
    sync_token TEXT,
    display_name TEXT,
    tax_registration_number TEXT,
    tax_tracked_on_sales BOOLEAN,
    tax_tracked_on_purchases BOOLEAN,
    tax_agency_config TEXT,
    qbo_created_at TIMESTAMPTZ,
    qbo_updated_at TIMESTAMPTZ,
    synced_at TIMESTAMPTZ DEFAULT NOW(),
    raw_data JSONB
);
