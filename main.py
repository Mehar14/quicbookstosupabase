from intuitlib.client import AuthClient
from intuitlib.enums import Scopes

# Initialize client
auth_client = AuthClient(
    client_id="",
    client_secret="",
    environment="sandbox",  # Change to "production" for live data
    redirect_uri="https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl"
)

# 1. Get Authorization URL
auth_url = auth_client.get_authorization_url([Scopes.ACCOUNTING])
print(f"Please visit this URL to authorize: {auth_url}")

access_token = ""
refresh_token = ""
print(f"Refresh Token: {refresh_token}")

from intuitlib.client import AuthClient
from quickbooks import QuickBooks
from quickbooks.objects.customer import Customer
from supabase import create_client, Client

# Configurations
QBO_CLIENT_ID = ""
QBO_CLIENT_SECRET = ""
QBO_REFRESH_TOKEN = ""
QBO_COMPANY_ID = ""

SUPABASE_URL = "https://flpkuyomxeaueimkpbdr.supabase.co"
SUPABASE_KEY = ""

# 1. Connect to Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. Refresh QuickBooks Tokens
auth_client = AuthClient(
    client_id=QBO_CLIENT_ID,
    client_secret=QBO_CLIENT_SECRET,
    environment="sandbox",
    redirect_uri="https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl"
)
auth_client.refresh(refresh_token=QBO_REFRESH_TOKEN)

# 3. Connect to QuickBooks API
qbo_client = QuickBooks(
    auth_client=auth_client,
    company_id=QBO_COMPANY_ID,
    minorversion=70
)

# 4. Fetch Customers from QuickBooks
customers = Customer.all(qb=qbo_client)

print(f"Fetched {len(customers)} customers from QuickBooks!")

for c in customers:
    print(f"{c.Id}, Customer: {c.DisplayName}, Email: {getattr(c.PrimaryEmailAddr, 'Address', 'N/A') if c.PrimaryEmailAddr else 'N/A'}, Balance: {c.Balance}")

# 5. Format and Sync Data to Supabase
formatted_customers = []
for c in customers:
    formatted_customers.append({
        "qbo_id": c.Id,
        "display_name": c.DisplayName,
        "email": getattr(c.PrimaryEmailAddr, 'Address', None) if c.PrimaryEmailAddr else None,
        "company_name": c.CompanyName,
        "balance": float(c.Balance) if c.Balance else 0.0
    })

# 6. Upsert data into Supabase (matches on 'qbo_id' primary key constraint)
if formatted_customers:
    response = supabase.table("qbo_customers").upsert(
        formatted_customers, 
        on_conflict="qbo_id"
    ).execute()
    print(f"Successfully synced {len(formatted_customers)} customers to Supabase!")