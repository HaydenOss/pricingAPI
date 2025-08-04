from pydantic import BaseModel

store_template = {
    "store_id": None,  # int (optional if auto-generated)
    "store_name": "",  # str
    "store_description": "",  # str (optional)
}

location_template = {
    "location_id": None,  # int (optional)
    "store_id": None,  # int FK → Store
    "street_address": "",  # str
    "state": "",  # str
    "zipcode": "",  # str
}

product_template = {
    "product_id": None,  # int (optional)
    "name": "",  # str
    "description": "",  # str (optional)
}

listing_template = {
    "listing_id": None,  # int (optional)
    "product_id": None,  # int FK → Product
    "location_id": None,  # int FK → Location
    "price": 0.0,  # float
    "scraped_at": None,  # datetime or ISO 8601 string
}


class Store(BaseModel):
    store_name: str
    store_description: str


class Products(BaseModel):
    prod_name: str
    description: str


class Locations(BaseModel):
    state: str
    zipcode: str
    town: str
    street_address: str
    store_id: int


class Listings(BaseModel):
    listing_id: int
    product_id: int
    location_id: int
    price: float
