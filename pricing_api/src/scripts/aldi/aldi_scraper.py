from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import time
import csv

from pricing_api.src.scripts.file_management import store_file_mngmt


def check_cookies():
    try:
        accept_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        accept_btn.click()
        print("Accepted cookies.")
        time.sleep(2)
    except:
        print("No cookie popup found.")


def create_soup(driver, link):
    # Open the page
    driver.get(link)
    time.sleep(2)
    check_cookies()
    return BeautifulSoup(driver.page_source, "html.parser")

def get_location():
    # Opening the location page
    locator = driver.find_element(
        By.CSS_SELECTOR,
        "div.select-merchant-feature-bar__service-address-wrapper > button",
    )
    if locator:
        locator.click()
        time.sleep(1.5)
    else:
        print("Locator not found for location")

    # Pulling the location data
    location_div = driver.find_element(
        By.CSS_SELECTOR,
        "div > button.base-button.base-button--primary-light-background",
    )

    if location_div:
        address = location_div.text
        add_split = address.split()
        print("Address: ", add_split)
    else:
        print("Location div not found.")

    return add_split[0], add_split[1], add_split[2]


# Parse all products
def get_prods(soup, total_prods_int, prod_count, writer):
    product_section = soup.select_one(
        "#main > section.container-layout.container-layout--padded > div > div > div.product-listing-viewer__product-area > div > div.product-listing-viewer__product-list-content > div"
    )
    products = product_section.find_all(recursive=False)

    for product in products:
        # Grabbing the HTML elements
        name_tag = product.select_one("div.product-tile__name")
        price_tag = product.select_one("span.base-price__regular > span")

        # Getting the text for the item
        name = name_tag.get_text(strip=True) if name_tag else "No name"
        price = price_tag.get_text(strip=True) if price_tag else "No price"

        # Writing the text to the file
        writer.writerow([name, price, "Aldi"])
        prod_count += 1

    print(
        "Number of prods pulled so far: " + str(prod_count) + "/" + str(total_prods_int)
    )
    if total_prods_int >= prod_count:
        return 0, prod_count
    else:
        print("Done pulling and saving prods")
        return 1, prod_count


def next_page(driver, pg_count, home_page):
    try:
        print("Clicking next page: " + str(pg_count))
        return create_soup(driver, (home_page + page_link + str(pg_count)))
    except Exception as e:
        print("Could not click next page:", e)



page_link = "?page="
home_page = "https://new.aldi.us/products"

options = Options()
# options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

print("________________________________________________")
check_cookies()
soup = create_soup(driver, home_page)

total_prods_item = soup.select_one(
    "#main > section.container-layout.container-layout--padded > div > div > div.product-listing-viewer__headline > div > h2 > span"
)

total_prods = total_prods_item.get_text()
total_prods = total_prods[1 : (len(total_prods) - 1)]
total_prods_int = int(total_prods)

pg_count = 1
product_count = 0

with open("./csv/aldi_products.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Product", "Price", "Store"])

    parsing_status_done = False

    while not parsing_status_done:
        parsing_status_done, product_count = get_prods(
            soup, total_prods_int, product_count, writer
        )

        pg_count += 1
        soup = next_page(driver, pg_count, home_page)
        print("________________________________________________")


print("All products are pulled from this location")

driver.quit()
