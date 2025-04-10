from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import time
import csv


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


# Parse all products
def pull_prods(soup, total_prods_int, prod_count, writer):
    product_section = soup.select_one(
        "#main > section.container-layout.container-layout--padded > div > div > div.product-listing-viewer__product-area > div > div.product-listing-viewer__product-list-content > div"
    )
    products = product_section.find_all(recursive=False)

    for product in products:
        # Grabbing the HTML elements
        name_tag = product.select_one("div.product-tile__name")
        price_tag = product.select_one("div.base-price span")

        # Getting the text for the item
        name = name_tag.get_text(strip=True) if name_tag else "No name"
        price = price_tag.get_text(strip=True) if price_tag else "No price"

        # print("Product: " + name)

        # Writing the text to the file
        writer.writerow([name, price, "Aldi"])
        prod_count += 1

    print(
        "Number of prods pulled so far: " + str(prod_count) + "/" + str(total_prods_int)
    )
    if total_prods_int != prod_count:
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


def create_soup(driver, link):
    # Open the page
    driver.get(link)
    time.sleep(2)
    check_cookies()
    return BeautifulSoup(driver.page_source, "html.parser")


page_link = "?page="
home_page = "https://new.aldi.us/products"

options = Options()
options.add_argument("--headless")
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

with open("../csv/aldi_products.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Product", "Price", "Store"])

    parsing_status_done = False

    while not parsing_status_done:
        parsing_status_done, product_count = pull_prods(
            soup, total_prods_int, product_count, writer
        )

        pg_count += 1
        soup = next_page(driver, pg_count, home_page)
        print("________________________________________________")


print("All products are pulled from this location")

driver.quit()
