from fastapi import APIRouter

# from app.schemas.schema import Listings, Locations, Products, Store
from app.services.aldi.aldi_locations import main

# from supabase_client import supabase

router = APIRouter()


@router.get("/aldi")
def aldi_downloads() -> dict:
    try:
        main()
        return {"status": 200, "message": "Successfully retrieved data"}
    except Exception as e:
        return {"status": 500, "message": "Failed to retrieve data", "error": str(e)}
