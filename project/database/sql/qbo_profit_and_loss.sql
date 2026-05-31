CREATE TABLE IF NOT EXISTS public.qbo_profit_and_loss (
    report_key TEXT PRIMARY KEY,
    start_period DATE,
    end_period DATE,
    report_name TEXT,
    report_basis TEXT,
    currency TEXT,
    generated_at TIMESTAMPTZ,
    synced_at TIMESTAMPTZ DEFAULT NOW(),
    raw_data JSONB
);
