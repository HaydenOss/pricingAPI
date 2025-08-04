# from app.schemas.schema import Listings, Locations, Products, Store
import supabase
from fastapi import APIRouter

router = APIRouter()


@router.get("/get-stores")
def get_stores() -> object:
    response = supabase.table("Stores").select("*").execute()
    print(response)
    return response
