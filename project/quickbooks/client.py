from quickbooks import QuickBooks

from config import QBO_COMPANY_ID
from authorization import get_auth_client


def get_qbo_client() -> QuickBooks:
    return QuickBooks(
        auth_client=get_auth_client(),
        company_id=QBO_COMPANY_ID,
        minorversion=70,
    )