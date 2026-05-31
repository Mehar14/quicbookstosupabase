from datetime import datetime


def empty_to_none(value):
    if value == "":
        return None
    return value


def ref_value(ref):
    if not ref:
        return None
    if isinstance(ref, dict):
        return ref.get("value")
    return getattr(ref, "value", None)


def ref_name(ref):
    if not ref:
        return None
    if isinstance(ref, dict):
        return ref.get("name")
    return getattr(ref, "name", None)


def phone_number(phone):
    if not phone:
        return None
    if isinstance(phone, dict):
        return phone.get("FreeFormNumber")
    return getattr(phone, "FreeFormNumber", None)


def email_address(email):
    if not email:
        return None
    if isinstance(email, dict):
        return email.get("Address")
    return getattr(email, "Address", None)


def web_address(web):
    if not web:
        return None
    if isinstance(web, dict):
        return web.get("URI")
    return getattr(web, "URI", None)


def address_fields(addr, prefix):
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
        f"{prefix}_line1": empty_to_none(addr.get("Line1")),
        f"{prefix}_line2": empty_to_none(addr.get("Line2")),
        f"{prefix}_city": empty_to_none(addr.get("City")),
        f"{prefix}_state": empty_to_none(addr.get("CountrySubDivisionCode")),
        f"{prefix}_postal_code": empty_to_none(addr.get("PostalCode")),
        f"{prefix}_country": empty_to_none(addr.get("Country")),
    }


def parse_qbo_timestamp(value):
    if not value:
        return None
    return datetime.fromisoformat(value)


def metadata_fields(data: dict) -> dict:
    metadata = data.get("MetaData") or {}
    created_at = parse_qbo_timestamp(metadata.get("CreateTime"))
    updated_at = parse_qbo_timestamp(metadata.get("LastUpdatedTime"))
    return {
        "qbo_created_at": created_at.isoformat() if created_at else None,
        "qbo_updated_at": updated_at.isoformat() if updated_at else None,
    }


def currency_fields(data: dict) -> dict:
    currency_ref = data.get("CurrencyRef") or {}
    if not isinstance(currency_ref, dict):
        return {"currency_code": None, "currency_name": None}
    return {
        "currency_code": currency_ref.get("value"),
        "currency_name": currency_ref.get("name"),
    }


def base_record(data: dict) -> dict:
    record = {
        "qbo_id": data["Id"],
        "sync_token": data.get("SyncToken"),
        "raw_data": data,
    }
    record.update(metadata_fields(data))
    return record
