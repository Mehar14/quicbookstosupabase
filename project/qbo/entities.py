from quickbooks.objects.account import Account
from quickbooks.objects.bill import Bill
from quickbooks.objects.company_info import CompanyInfo
from quickbooks.objects.customer import Customer
from quickbooks.objects.employee import Employee
from quickbooks.objects.estimate import Estimate
from quickbooks.objects.invoice import Invoice
from quickbooks.objects.item import Item
from quickbooks.objects.payment import Payment
from quickbooks.objects.preferences import Preferences
from quickbooks.objects.taxagency import TaxAgency
from quickbooks.objects.vendor import Vendor

from config import PROFIT_AND_LOSS_END_DATE, PROFIT_AND_LOSS_START_DATE


def fetch_accounts(qbo_client):
    return Account.all(qb=qbo_client)


def fetch_bills(qbo_client):
    return Bill.all(qb=qbo_client)


def fetch_company_info(qbo_client):
    return CompanyInfo.all(qb=qbo_client)


def fetch_customers(qbo_client):
    return Customer.all(qb=qbo_client)


def fetch_employees(qbo_client):
    return Employee.all(qb=qbo_client)


def fetch_estimates(qbo_client):
    return Estimate.all(qb=qbo_client)


def fetch_invoices(qbo_client):
    return Invoice.all(qb=qbo_client)


def fetch_items(qbo_client):
    return Item.all(qb=qbo_client)


def fetch_payments(qbo_client):
    return Payment.all(qb=qbo_client)


def fetch_preferences(qbo_client):
    return [Preferences.get(qb=qbo_client)]


def fetch_tax_agencies(qbo_client):
    return TaxAgency.all(qb=qbo_client)


def fetch_vendors(qbo_client):
    return Vendor.all(qb=qbo_client)


def fetch_profit_and_loss(qbo_client):
    report = qbo_client.get_report(
        "ProfitAndLoss",
        {
            "start_date": PROFIT_AND_LOSS_START_DATE,
            "end_date": PROFIT_AND_LOSS_END_DATE,
        },
    )
    return [report]
