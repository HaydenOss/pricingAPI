# from app.schemas.schema import Listings, Locations, Products, Store
from fastapi import APIRouter

from app.server.connection import supabase

router = APIRouter()


@router.get("/get-stores")
def get_stores() -> object:
    print("in getting stores")

    try:

        response = supabase.table("stores").select("*").execute()
        print("Data:", response.data)
        return {
            "status": 200,
            "data": response,
        }
    except Exception as e:
        print("An error occurred while pulling the stores: ", e)
        return {"status": 500}
