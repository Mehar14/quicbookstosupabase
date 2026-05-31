from pathlib import Path

import psycopg2
from postgrest.exceptions import APIError
from supabase import Client

from config import SUPABASE_DB_URL

SQL_DIR = Path(__file__).parent / "sql"


def _read_sql(filename: str) -> str:
    return (SQL_DIR / filename).read_text()


def _split_sql_statements(sql: str) -> list[str]:
    return [statement.strip() for statement in sql.split(";") if statement.strip()]


QBO_CUSTOMERS_CREATE_SQL = _read_sql("qbo_customers.sql")
QBO_CUSTOMERS_CREATE_STATEMENTS = _split_sql_statements(QBO_CUSTOMERS_CREATE_SQL)


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
                "Could not create qbo_customers table automatically. Either:\n"
                "1. Add SUPABASE_DB_URL to .env (Supabase Settings > Database > Connection string), or\n"
                "2. Run database/sql/bootstrap_exec_sql.sql once in the Supabase SQL editor, then rerun."
            ) from error
        raise


def ensure_qbo_customers_table(supabase_client: Client | None = None) -> None:
    if SUPABASE_DB_URL:
        _execute_with_psycopg(QBO_CUSTOMERS_CREATE_STATEMENTS)
    elif supabase_client is not None:
        _execute_with_rpc(supabase_client, QBO_CUSTOMERS_CREATE_STATEMENTS)
    else:
        raise ValueError(
            "Set SUPABASE_DB_URL or create the public.exec_sql RPC function "
            "and pass a Supabase client to create tables."
        )

    print("Ensured qbo_customers table exists")
