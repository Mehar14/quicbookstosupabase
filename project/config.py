import os
from dotenv import load_dotenv

load_dotenv()

QBO_CLIENT_ID = os.getenv("QBO_CLIENT_ID")
QBO_CLIENT_SECRET = os.getenv("QBO_CLIENT_SECRET")
QBO_REFRESH_TOKEN = os.getenv("QBO_REFRESH_TOKEN")
QBO_COMPANY_ID = os.getenv("QBO_COMPANY_ID")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

QBO_REDIRECT_URI = (
    "https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl"
)