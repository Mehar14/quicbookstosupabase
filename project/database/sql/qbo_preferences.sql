CREATE TABLE IF NOT EXISTS public.qbo_preferences (
    qbo_id TEXT PRIMARY KEY,
    sync_token TEXT,
    qbo_created_at TIMESTAMPTZ,
    qbo_updated_at TIMESTAMPTZ,
    synced_at TIMESTAMPTZ DEFAULT NOW(),
    raw_data JSONB
);
