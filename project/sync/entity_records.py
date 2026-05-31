from sync.common import (
    address_fields,
    base_record,
    currency_fields,
    email_address,
    empty_to_none,
    metadata_fields,
    parse_qbo_timestamp,
    phone_number,
    ref_name,
    ref_value,
    web_address,
)


def account_to_record(account) -> dict:
    data = account.to_dict()
    record = base_record(data)
    record.update({
        "name": empty_to_none(data.get("Name")),
        "fully_qualified_name": empty_to_none(data.get("FullyQualifiedName")),
        "active": data.get("Active"),
        "sub_account": data.get("SubAccount"),
        "classification": empty_to_none(data.get("Classification")),
        "account_type": empty_to_none(data.get("AccountType")),
        "account_sub_type": empty_to_none(data.get("AccountSubType")),
        "description": empty_to_none(data.get("Description")),
        "acct_num": empty_to_none(data.get("AcctNum")),
        "current_balance": data.get("CurrentBalance"),
        "current_balance_with_sub_accounts": data.get("CurrentBalanceWithSubAccounts"),
        "parent_ref": ref_value(data.get("ParentRef")),
        "tax_code_ref": ref_value(data.get("TaxCodeRef")),
    })
    record.update(currency_fields(data))
    return record


def bill_to_record(bill) -> dict:
    data = bill.to_dict()
    record = base_record(data)
    record.update({
        "due_date": empty_to_none(data.get("DueDate")),
        "balance": data.get("Balance"),
        "total_amt": data.get("TotalAmt"),
        "txn_date": empty_to_none(data.get("TxnDate")),
        "doc_number": empty_to_none(data.get("DocNumber")),
        "private_note": empty_to_none(data.get("PrivateNote")),
        "exchange_rate": data.get("ExchangeRate"),
        "global_tax_calculation": empty_to_none(data.get("GlobalTaxCalculation")),
        "sales_term_ref": ref_value(data.get("SalesTermRef")),
        "vendor_ref": ref_value(data.get("VendorRef")),
        "vendor_name": ref_name(data.get("VendorRef")),
        "department_ref": ref_value(data.get("DepartmentRef")),
        "ap_account_ref": ref_value(data.get("APAccountRef")),
    })
    record.update(currency_fields(data))
    record.update(address_fields(data.get("VendorAddr"), "vendor_addr"))
    return record


def company_info_to_record(company_info) -> dict:
    data = company_info.to_dict()
    record = base_record(data)
    record.update({
        "company_name": empty_to_none(data.get("CompanyName")),
        "legal_name": empty_to_none(data.get("LegalName")),
        "company_start_date": empty_to_none(data.get("CompanyStartDate")),
        "fiscal_year_start_month": empty_to_none(data.get("FiscalYearStartMonth")),
        "country": empty_to_none(data.get("Country")),
        "supported_languages": empty_to_none(data.get("SupportedLanguages")),
        "default_time_zone": empty_to_none(data.get("DefaultTimeZone")),
        "primary_phone": phone_number(data.get("PrimaryPhone")),
        "email": email_address(data.get("Email")),
        "web_addr": web_address(data.get("WebAddr")),
    })
    record.update(address_fields(data.get("CompanyAddr"), "company_addr"))
    record.update(address_fields(data.get("LegalAddr"), "legal_addr"))
    return record


def customer_to_record(customer) -> dict:
    data = customer.to_dict()
    record = base_record(data)
    record.update({
        "title": empty_to_none(data.get("Title")),
        "given_name": empty_to_none(data.get("GivenName")),
        "middle_name": empty_to_none(data.get("MiddleName")),
        "family_name": empty_to_none(data.get("FamilyName")),
        "suffix": empty_to_none(data.get("Suffix")),
        "fully_qualified_name": empty_to_none(data.get("FullyQualifiedName")),
        "company_name": empty_to_none(data.get("CompanyName")),
        "display_name": empty_to_none(data.get("DisplayName")),
        "print_on_check_name": empty_to_none(data.get("PrintOnCheckName")),
        "notes": empty_to_none(data.get("Notes")),
        "active": data.get("Active"),
        "is_project": data.get("IsProject"),
        "job": data.get("Job"),
        "bill_with_parent": data.get("BillWithParent"),
        "taxable": data.get("Taxable"),
        "balance": data.get("Balance"),
        "balance_with_jobs": data.get("BalanceWithJobs"),
        "preferred_delivery_method": empty_to_none(data.get("PreferredDeliveryMethod")),
        "resale_num": empty_to_none(data.get("ResaleNum")),
        "level": data.get("Level"),
        "open_balance_date": empty_to_none(data.get("OpenBalanceDate")),
        "primary_tax_identifier": empty_to_none(data.get("PrimaryTaxIdentifier")),
        "primary_phone": phone_number(data.get("PrimaryPhone")),
        "alternate_phone": phone_number(data.get("AlternatePhone")),
        "mobile": phone_number(data.get("Mobile")),
        "fax": phone_number(data.get("Fax")),
        "primary_email": email_address(data.get("PrimaryEmailAddr")),
        "web_addr": web_address(data.get("WebAddr")),
        "default_tax_code_ref": ref_value(data.get("DefaultTaxCodeRef")),
        "sales_term_ref": ref_value(data.get("SalesTermRef")),
        "payment_method_ref": ref_value(data.get("PaymentMethodRef")),
        "parent_ref": ref_value(data.get("ParentRef")),
        "ar_account_ref": ref_value(data.get("ARAccountRef")),
        "client_entity_id": empty_to_none(data.get("ClientEntityId")),
        "v4_id_pseudonym": empty_to_none(data.get("V4IDPseudonym")),
    })
    record.update(currency_fields(data))
    record.update(address_fields(data.get("BillAddr"), "bill_addr"))
    record.update(address_fields(data.get("ShipAddr"), "ship_addr"))
    return record


def employee_to_record(employee) -> dict:
    data = employee.to_dict()
    record = base_record(data)
    record.update({
        "given_name": empty_to_none(data.get("GivenName")),
        "middle_name": empty_to_none(data.get("MiddleName")),
        "family_name": empty_to_none(data.get("FamilyName")),
        "suffix": empty_to_none(data.get("Suffix")),
        "display_name": empty_to_none(data.get("DisplayName")),
        "print_on_check_name": empty_to_none(data.get("PrintOnCheckName")),
        "employee_number": empty_to_none(data.get("EmployeeNumber")),
        "title": empty_to_none(data.get("Title")),
        "bill_rate": data.get("BillRate"),
        "cost_rate": data.get("CostRate"),
        "birth_date": empty_to_none(data.get("BirthDate")),
        "gender": empty_to_none(data.get("Gender")),
        "hired_date": empty_to_none(data.get("HiredDate")),
        "released_date": empty_to_none(data.get("ReleasedDate")),
        "active": data.get("Active"),
        "organization": data.get("Organization"),
        "billable_time": data.get("BillableTime"),
        "primary_phone": phone_number(data.get("PrimaryPhone")),
        "mobile": phone_number(data.get("Mobile")),
        "email": email_address(data.get("EmailAddress")),
        "v4_id_pseudonym": empty_to_none(data.get("V4IDPseudonym")),
    })
    record.update(address_fields(data.get("PrimaryAddr"), "primary_addr"))
    return record


def estimate_to_record(estimate) -> dict:
    data = estimate.to_dict()
    record = base_record(data)
    record.update({
        "doc_number": empty_to_none(data.get("DocNumber")),
        "txn_date": empty_to_none(data.get("TxnDate")),
        "txn_status": empty_to_none(data.get("TxnStatus")),
        "private_note": empty_to_none(data.get("PrivateNote")),
        "total_amt": data.get("TotalAmt"),
        "exchange_rate": data.get("ExchangeRate"),
        "apply_tax_after_discount": data.get("ApplyTaxAfterDiscount"),
        "print_status": empty_to_none(data.get("PrintStatus")),
        "email_status": empty_to_none(data.get("EmailStatus")),
        "due_date": empty_to_none(data.get("DueDate")),
        "ship_date": empty_to_none(data.get("ShipDate")),
        "expiration_date": empty_to_none(data.get("ExpirationDate")),
        "accepted_by": empty_to_none(data.get("AcceptedBy")),
        "accepted_date": empty_to_none(data.get("AcceptedDate")),
        "global_tax_calculation": empty_to_none(data.get("GlobalTaxCalculation")),
        "customer_ref": ref_value(data.get("CustomerRef")),
        "customer_name": ref_name(data.get("CustomerRef")),
        "project_ref": ref_value(data.get("ProjectRef")),
        "department_ref": ref_value(data.get("DepartmentRef")),
        "class_ref": ref_value(data.get("ClassRef")),
        "sales_term_ref": ref_value(data.get("SalesTermRef")),
        "ship_method_ref": ref_value(data.get("ShipMethodRef")),
        "tracking_num": empty_to_none(data.get("TrackingNum")),
        "free_form_address": data.get("FreeFormAddress"),
    })
    record.update(currency_fields(data))
    record.update(address_fields(data.get("BillAddr"), "bill_addr"))
    record.update(address_fields(data.get("ShipAddr"), "ship_addr"))
    return record


def invoice_to_record(invoice) -> dict:
    data = invoice.to_dict()
    record = base_record(data)
    record.update({
        "doc_number": empty_to_none(data.get("DocNumber")),
        "txn_date": empty_to_none(data.get("TxnDate")),
        "due_date": empty_to_none(data.get("DueDate")),
        "ship_date": empty_to_none(data.get("ShipDate")),
        "private_note": empty_to_none(data.get("PrivateNote")),
        "total_amt": data.get("TotalAmt"),
        "balance": data.get("Balance"),
        "deposit": data.get("Deposit"),
        "home_total_amt": data.get("HomeTotalAmt"),
        "home_balance": data.get("HomeBalance"),
        "exchange_rate": data.get("ExchangeRate"),
        "apply_tax_after_discount": data.get("ApplyTaxAfterDiscount"),
        "print_status": empty_to_none(data.get("PrintStatus")),
        "email_status": empty_to_none(data.get("EmailStatus")),
        "global_tax_calculation": empty_to_none(data.get("GlobalTaxCalculation")),
        "invoice_link": empty_to_none(data.get("InvoiceLink")),
        "e_invoice_status": empty_to_none(data.get("EInvoiceStatus")),
        "tracking_num": empty_to_none(data.get("TrackingNum")),
        "free_form_address": data.get("FreeFormAddress"),
        "allow_online_payment": data.get("AllowOnlinePayment"),
        "allow_ipn_payment": data.get("AllowIPNPayment"),
        "allow_online_credit_card_payment": data.get("AllowOnlineCreditCardPayment"),
        "allow_online_ach_payment": data.get("AllowOnlineACHPayment"),
        "customer_ref": ref_value(data.get("CustomerRef")),
        "customer_name": ref_name(data.get("CustomerRef")),
        "department_ref": ref_value(data.get("DepartmentRef")),
        "sales_term_ref": ref_value(data.get("SalesTermRef")),
        "ship_method_ref": ref_value(data.get("ShipMethodRef")),
        "tax_exemption_ref": ref_value(data.get("TaxExemptionRef")),
    })
    record.update(currency_fields(data))
    record.update(address_fields(data.get("BillAddr"), "bill_addr"))
    record.update(address_fields(data.get("ShipAddr"), "ship_addr"))
    return record


def item_to_record(item) -> dict:
    data = item.to_dict()
    record = base_record(data)
    record.update({
        "name": empty_to_none(data.get("Name")),
        "description": empty_to_none(data.get("Description")),
        "active": data.get("Active"),
        "sub_item": data.get("SubItem"),
        "fully_qualified_name": empty_to_none(data.get("FullyQualifiedName")),
        "taxable": data.get("Taxable"),
        "sales_tax_included": data.get("SalesTaxIncluded"),
        "unit_price": data.get("UnitPrice"),
        "type": empty_to_none(data.get("Type")),
        "level": data.get("Level"),
        "purchase_desc": empty_to_none(data.get("PurchaseDesc")),
        "purchase_tax_included": data.get("PurchaseTaxIncluded"),
        "purchase_cost": data.get("PurchaseCost"),
        "track_qty_on_hand": data.get("TrackQtyOnHand"),
        "qty_on_hand": data.get("QtyOnHand"),
        "inv_start_date": empty_to_none(data.get("InvStartDate")),
        "sku": empty_to_none(data.get("Sku")),
        "service_type": empty_to_none(data.get("ServiceType")),
        "item_category_type": empty_to_none(data.get("ItemCategoryType")),
        "asset_account_ref": ref_value(data.get("AssetAccountRef")),
        "expense_account_ref": ref_value(data.get("ExpenseAccountRef")),
        "income_account_ref": ref_value(data.get("IncomeAccountRef")),
        "sales_tax_code_ref": ref_value(data.get("SalesTaxCodeRef")),
        "parent_ref": ref_value(data.get("ParentRef")),
        "purchase_tax_code_ref": ref_value(data.get("PurchaseTaxCodeRef")),
    })
    return record


def payment_to_record(payment) -> dict:
    data = payment.to_dict()
    record = base_record(data)
    record.update({
        "payment_ref_num": empty_to_none(data.get("PaymentRefNum")),
        "total_amt": data.get("TotalAmt"),
        "unapplied_amt": data.get("UnappliedAmt"),
        "exchange_rate": data.get("ExchangeRate"),
        "txn_date": empty_to_none(data.get("TxnDate")),
        "txn_source": empty_to_none(data.get("TxnSource")),
        "private_note": empty_to_none(data.get("PrivateNote")),
        "txn_status": empty_to_none(data.get("TxnStatus")),
        "transaction_location_type": empty_to_none(data.get("TransactionLocationType")),
        "process_payment": data.get("ProcessPayment"),
        "customer_ref": ref_value(data.get("CustomerRef")),
        "customer_name": ref_name(data.get("CustomerRef")),
        "ar_account_ref": ref_value(data.get("ARAccountRef")),
        "payment_method_ref": ref_value(data.get("PaymentMethodRef")),
        "deposit_to_account_ref": ref_value(data.get("DepositToAccountRef")),
        "tax_exemption_ref": ref_value(data.get("TaxExemptionRef")),
    })
    record.update(currency_fields(data))
    return record


def preferences_to_record(preferences) -> dict:
    data = preferences.to_dict()
    return {
        "qbo_id": data.get("Id") or "1",
        "sync_token": data.get("SyncToken"),
        "raw_data": data,
        **metadata_fields(data),
    }


def profit_and_loss_to_record(report: dict) -> dict:
    header = report.get("Header") or {}
    start_period = header.get("StartPeriod")
    end_period = header.get("EndPeriod")
    generated_at = parse_qbo_timestamp(header.get("Time"))
    return {
        "report_key": f"{start_period}|{end_period}",
        "start_period": start_period,
        "end_period": end_period,
        "report_name": header.get("ReportName"),
        "report_basis": header.get("ReportBasis"),
        "currency": header.get("Currency"),
        "generated_at": generated_at.isoformat() if generated_at else None,
        "raw_data": report,
    }


def tax_agency_to_record(tax_agency) -> dict:
    data = tax_agency.to_dict()
    record = base_record(data)
    record.update({
        "display_name": empty_to_none(data.get("DisplayName")),
        "tax_registration_number": empty_to_none(data.get("TaxRegistrationNumber")),
        "tax_tracked_on_sales": data.get("TaxTrackedOnSales"),
        "tax_tracked_on_purchases": data.get("TaxTrackedOnPurchases"),
        "tax_agency_config": empty_to_none(data.get("TaxAgencyConfig")),
    })
    return record


def vendor_to_record(vendor) -> dict:
    data = vendor.to_dict()
    record = base_record(data)
    record.update({
        "title": empty_to_none(data.get("Title")),
        "given_name": empty_to_none(data.get("GivenName")),
        "middle_name": empty_to_none(data.get("MiddleName")),
        "family_name": empty_to_none(data.get("FamilyName")),
        "suffix": empty_to_none(data.get("Suffix")),
        "company_name": empty_to_none(data.get("CompanyName")),
        "display_name": empty_to_none(data.get("DisplayName")),
        "print_on_check_name": empty_to_none(data.get("PrintOnCheckName")),
        "active": data.get("Active"),
        "tax_identifier": empty_to_none(data.get("TaxIdentifier")),
        "balance": data.get("Balance"),
        "bill_rate": data.get("BillRate"),
        "acct_num": empty_to_none(data.get("AcctNum")),
        "vendor_1099": data.get("Vendor1099"),
        "tax_reporting_basis": empty_to_none(data.get("TaxReportingBasis")),
        "primary_phone": phone_number(data.get("PrimaryPhone")),
        "alternate_phone": phone_number(data.get("AlternatePhone")),
        "mobile": phone_number(data.get("Mobile")),
        "fax": phone_number(data.get("Fax")),
        "primary_email": email_address(data.get("PrimaryEmailAddr")),
        "web_addr": web_address(data.get("WebAddr")),
        "term_ref": ref_value(data.get("TermRef")),
        "ap_account_ref": ref_value(data.get("APAccountRef")),
        "v4_id_pseudonym": empty_to_none(data.get("V4IDPseudonym")),
    })
    record.update(currency_fields(data))
    record.update(address_fields(data.get("BillAddr"), "bill_addr"))
    return record
