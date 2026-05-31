from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

def get_supabase_client() -> Client:
    print('getting supabase client')
    print(SUPABASE_URL, SUPABASE_KEY)
    return create_client(SUPABASE_URL, SUPABASE_KEY)