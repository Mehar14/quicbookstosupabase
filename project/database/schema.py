from pathlib import Path

import psycopg2
from postgrest.exceptions import APIError
from supabase import Client

from config import SUPABASE_DB_URL
from sync.registry import ENTITY_SYNC_CONFIGS

SQL_DIR = Path(__file__).parent / "sql"


def _read_sql(filename: str) -> str:
    return (SQL_DIR / filename).read_text()


def _split_sql_statements(sql: str) -> list[str]:
    return [statement.strip() for statement in sql.split(";") if statement.strip()]


def _execute_with_psycopg(statements: list[str]) -> None:
    if not SUPABASE_DB_URL:
        raise ValueError(
            "SUPABASE_DB_URL is required to run DDL. "
            "Add your Postgres connection string from Supabase project settings."
        )

    with psycopg2.connect(SUPABASE_DB_URL) as conn:
        with conn.cursor() as cursor:
            for statement in statements:
                cursor.execute(statement)
        conn.commit()


def _execute_with_rpc(supabase_client: Client, statements: list[str]) -> None:
    try:
        for statement in statements:
            supabase_client.rpc("exec_sql", {"query": statement}).execute()
    except APIError as error:
        if error.code == "PGRST202":
            raise ValueError(
                "Could not create QBO tables automatically. Either:\n"
                "1. Add SUPABASE_DB_URL to .env (Supabase Settings > Database > Connection string), or\n"
                "2. Run database/sql/bootstrap_exec_sql.sql once in the Supabase SQL editor, then rerun."
            ) from error
        raise


def _ensure_table(sql_file: str, supabase_client: Client | None = None) -> None:
    statements = _split_sql_statements(_read_sql(sql_file))

    if SUPABASE_DB_URL:
        _execute_with_psycopg(statements)
    elif supabase_client is not None:
        _execute_with_rpc(supabase_client, statements)
    else:
        raise ValueError(
            "Set SUPABASE_DB_URL or create the public.exec_sql RPC function "
            "and pass a Supabase client to create tables."
        )


def ensure_all_qbo_tables(supabase_client: Client | None = None) -> None:
    for config in ENTITY_SYNC_CONFIGS:
        _ensure_table(config.sql_file, supabase_client=supabase_client)
        print(f"Ensured {config.table} table exists")
