from datetime import datetime

from qbo.customers import fetch_customers
from database.supabase_client import upsert_qbo_customers


def _empty_to_none(value):
    if value == "":
        return None
    return value


def _ref_value(ref):
    if not ref:
        return None
    if isinstance(ref, dict):
        return ref.get("value")
    return getattr(ref, "value", None)


def _phone_number(phone):
    if not phone:
        return None
    if isinstance(phone, dict):
        return phone.get("FreeFormNumber")
    return getattr(phone, "FreeFormNumber", None)


def _email_address(email):
    if not email:
        return None
    if isinstance(email, dict):
        return email.get("Address")
    return getattr(email, "Address", None)


def _web_address(web):
    if not web:
        return None
    if isinstance(web, dict):
        return web.get("URI")
    return getattr(web, "URI", None)


def _address_fields(addr, prefix):
    if not addr:
        return {
            f"{prefix}_line1": None,
            f"{prefix}_line2": None,
            f"{prefix}_city": None,
            f"{prefix}_state": None,
            f"{prefix}_postal_code": None,
            f"{prefix}_country": None,
        }

    if not isinstance(addr, dict):
        addr = addr.to_dict() if hasattr(addr, "to_dict") else {}

    return {
        f"{prefix}_line1": _empty_to_none(addr.get("Line1")),
        f"{prefix}_line2": _empty_to_none(addr.get("Line2")),
        f"{prefix}_city": _empty_to_none(addr.get("City")),
        f"{prefix}_state": _empty_to_none(addr.get("CountrySubDivisionCode")),
        f"{prefix}_postal_code": _empty_to_none(addr.get("PostalCode")),
        f"{prefix}_country": _empty_to_none(addr.get("Country")),
    }


def _parse_qbo_timestamp(value):
    if not value:
        return None
    return datetime.fromisoformat(value)


def customer_to_record(customer) -> dict:
    data = customer.to_dict()

    currency_ref = data.get("CurrencyRef") or {}
    metadata = data.get("MetaData") or {}

    qbo_created_at = _parse_qbo_timestamp(metadata.get("CreateTime"))
    qbo_updated_at = _parse_qbo_timestamp(metadata.get("LastUpdatedTime"))

    record = {
        "qbo_id": data["Id"],
        "sync_token": data.get("SyncToken"),
        "title": _empty_to_none(data.get("Title")),
        "given_name": _empty_to_none(data.get("GivenName")),
        "middle_name": _empty_to_none(data.get("MiddleName")),
        "family_name": _empty_to_none(data.get("FamilyName")),
        "suffix": _empty_to_none(data.get("Suffix")),
        "fully_qualified_name": _empty_to_none(data.get("FullyQualifiedName")),
        "company_name": _empty_to_none(data.get("CompanyName")),
        "display_name": _empty_to_none(data.get("DisplayName")),
        "print_on_check_name": _empty_to_none(data.get("PrintOnCheckName")),
        "notes": _empty_to_none(data.get("Notes")),
        "active": data.get("Active"),
        "is_project": data.get("IsProject"),
        "job": data.get("Job"),
        "bill_with_parent": data.get("BillWithParent"),
        "taxable": data.get("Taxable"),
        "balance": data.get("Balance"),
        "balance_with_jobs": data.get("BalanceWithJobs"),
        "preferred_delivery_method": _empty_to_none(data.get("PreferredDeliveryMethod")),
        "resale_num": _empty_to_none(data.get("ResaleNum")),
        "level": data.get("Level"),
        "open_balance_date": _empty_to_none(data.get("OpenBalanceDate")),
        "primary_tax_identifier": _empty_to_none(data.get("PrimaryTaxIdentifier")),
        "primary_phone": _phone_number(data.get("PrimaryPhone")),
        "alternate_phone": _phone_number(data.get("AlternatePhone")),
        "mobile": _phone_number(data.get("Mobile")),
        "fax": _phone_number(data.get("Fax")),
        "primary_email": _email_address(data.get("PrimaryEmailAddr")),
        "web_addr": _web_address(data.get("WebAddr")),
        "default_tax_code_ref": _ref_value(data.get("DefaultTaxCodeRef")),
        "sales_term_ref": _ref_value(data.get("SalesTermRef")),
        "payment_method_ref": _ref_value(data.get("PaymentMethodRef")),
        "parent_ref": _ref_value(data.get("ParentRef")),
        "ar_account_ref": _ref_value(data.get("ARAccountRef")),
        "currency_code": currency_ref.get("value") if isinstance(currency_ref, dict) else None,
        "currency_name": currency_ref.get("name") if isinstance(currency_ref, dict) else None,
        "client_entity_id": _empty_to_none(data.get("ClientEntityId")),
        "v4_id_pseudonym": _empty_to_none(data.get("V4IDPseudonym")),
        "qbo_created_at": qbo_created_at.isoformat() if qbo_created_at else None,
        "qbo_updated_at": qbo_updated_at.isoformat() if qbo_updated_at else None,
        "raw_data": data,
    }

    record.update(_address_fields(data.get("BillAddr"), "bill_addr"))
    record.update(_address_fields(data.get("ShipAddr"), "ship_addr"))

    return record


def transform_customers(qbo_client) -> list[dict]:
    customers = fetch_customers(qbo_client)
    return [customer_to_record(customer) for customer in customers]


def sync_customers_to_supabase(qbo_client, supabase_client) -> None:
    records = transform_customers(qbo_client)

    if not records:
        print("No customers to sync")
        return

    upsert_qbo_customers(supabase_client, records)
    print(f"Synced {len(records)} customers")
