from dataclasses import dataclass
from typing import Callable

from qbo import entities as qbo_entities
from sync import entity_records


@dataclass(frozen=True)
class EntitySyncConfig:
    name: str
    table: str
    sql_file: str
    fetch: Callable
    transform: Callable
    conflict_column: str = "qbo_id"


ENTITY_SYNC_CONFIGS = [
    EntitySyncConfig(
        name="accounts",
        table="qbo_accounts",
        sql_file="qbo_accounts.sql",
        fetch=qbo_entities.fetch_accounts,
        transform=entity_records.account_to_record,
    ),
    EntitySyncConfig(
        name="bills",
        table="qbo_bills",
        sql_file="qbo_bills.sql",
        fetch=qbo_entities.fetch_bills,
        transform=entity_records.bill_to_record,
    ),
    EntitySyncConfig(
        name="company_info",
        table="qbo_company_info",
        sql_file="qbo_company_info.sql",
        fetch=qbo_entities.fetch_company_info,
        transform=entity_records.company_info_to_record,
    ),
    EntitySyncConfig(
        name="customers",
        table="qbo_customers",
        sql_file="qbo_customers.sql",
        fetch=qbo_entities.fetch_customers,
        transform=entity_records.customer_to_record,
    ),
    EntitySyncConfig(
        name="employees",
        table="qbo_employees",
        sql_file="qbo_employees.sql",
        fetch=qbo_entities.fetch_employees,
        transform=entity_records.employee_to_record,
    ),
    EntitySyncConfig(
        name="estimates",
        table="qbo_estimates",
        sql_file="qbo_estimates.sql",
        fetch=qbo_entities.fetch_estimates,
        transform=entity_records.estimate_to_record,
    ),
    EntitySyncConfig(
        name="invoices",
        table="qbo_invoices",
        sql_file="qbo_invoices.sql",
        fetch=qbo_entities.fetch_invoices,
        transform=entity_records.invoice_to_record,
    ),
    EntitySyncConfig(
        name="items",
        table="qbo_items",
        sql_file="qbo_items.sql",
        fetch=qbo_entities.fetch_items,
        transform=entity_records.item_to_record,
    ),
    EntitySyncConfig(
        name="payments",
        table="qbo_payments",
        sql_file="qbo_payments.sql",
        fetch=qbo_entities.fetch_payments,
        transform=entity_records.payment_to_record,
    ),
    EntitySyncConfig(
        name="preferences",
        table="qbo_preferences",
        sql_file="qbo_preferences.sql",
        fetch=qbo_entities.fetch_preferences,
        transform=entity_records.preferences_to_record,
    ),
    EntitySyncConfig(
        name="profit_and_loss",
        table="qbo_profit_and_loss",
        sql_file="qbo_profit_and_loss.sql",
        fetch=qbo_entities.fetch_profit_and_loss,
        transform=entity_records.profit_and_loss_to_record,
        conflict_column="report_key",
    ),
    EntitySyncConfig(
        name="tax_agencies",
        table="qbo_tax_agencies",
        sql_file="qbo_tax_agencies.sql",
        fetch=qbo_entities.fetch_tax_agencies,
        transform=entity_records.tax_agency_to_record,
    ),
    EntitySyncConfig(
        name="vendors",
        table="qbo_vendors",
        sql_file="qbo_vendors.sql",
        fetch=qbo_entities.fetch_vendors,
        transform=entity_records.vendor_to_record,
    ),
]
