import requests
from bs4 import BeautifulSoup

# URL of the ALDI products page
url = 'https://new.aldi.us/products'

# Send a GET request to the URL
response = requests.get(url)
response.raise_for_status()  # Raise an error for bad status codes

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Optional: Get store location (if it's somewhere in the page)
store_location = soup.select_one('div.store-locator-store-details')
store_text = store_location.get_text(strip=True) if store_location else "Unknown Store"

# Grab all product tiles
products = soup.select('div.product-tile')

count = 0
for product in products:
    # Get product name
    name_tag = product.select_one('div.product-tile__name')
    name = name_tag.get_text(strip=True) if name_tag else "No name"

    # Get product price
    price_tag = product.select_one('div.base-price span')
    price = price_tag.get_text(strip=True) if price_tag else "No price"
    count += 1
    # print(f"Product: {name}")
    # print(f"Price: {price}")
    # print(f"Store: {store_text}")
    # print("-" * 40)
print(count)
