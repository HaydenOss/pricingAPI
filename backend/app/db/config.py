import os

from dotenv import load_dotenv

load_dotenv()

debug = os.getenv("DEBUG") == "True"


def get_api_key() -> str:
    db_key = os.getenv("SUPABASE_KEY")
    return db_key


def get_api_url() -> str:
    db_url = os.getenv("SUPABASE_URL")
    return db_url
