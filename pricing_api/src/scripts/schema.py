store_template = {
    "store_id": None,              # int (optional if auto-generated)
    "name": "",                    # str
    "description": ""              # str (optional)
}

location_template = {
    "location_id": None,           # int (optional)
    "store_id": None,              # int FK → Store
    "street_address": "",          # str
    "state": "",                   # str
    "zip": ""                      # str
}

product_template = {
    "product_id": None,            # int (optional)
    "name": "",                    # str
    "description": ""              # str (optional)
}

listing_template = {
    "listing_id": None,            # int (optional)
    "product_id": None,            # int FK → Product
    "location_id": None,           # int FK → Location
    "price": 0.0,                  # float
    "scraped_at": None             # datetime or ISO 8601 string
}
