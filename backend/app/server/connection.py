from supabase import Client, create_client

from app.db.config import get_api_key, get_api_url

supabase_url = get_api_url()
supabase_key = get_api_key()

supabase: Client = create_client(supabase_url, supabase_key)
