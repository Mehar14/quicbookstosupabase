-- Run once in the Supabase SQL editor if you do not set SUPABASE_DB_URL.
CREATE OR REPLACE FUNCTION public.exec_sql(query text)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
    EXECUTE query;
END;
$$;
