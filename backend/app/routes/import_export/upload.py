from fastapi import APIRouter

from app.schemas.schema import Listings, Locations, Products, Store

# from supabase_client import supabase

router = APIRouter()


@router.post("/locations")
def locations_upload(locations: Locations) -> None:
    print("Locations: " + locations)
    # result = supabase.table("Locations").insert(locations.dict()).execute()

    # if result.error:
    #     raise HTTPException(status_code=400, detail=result.error.message)

    # return {"message": "Locations pushed: ", "Locations": result.data}
    # return None


@router.post("/store")
def store_upload(stores: Store) -> None:
    print(stores)
    return None


@router.post("/products")
def products_upload(products: Products) -> None:
    print(products)
    return None


@router.post("/listings")
def listings_upload(listings: Listings) -> None:
    print(listings)
    return None
