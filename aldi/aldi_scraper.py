from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import hashlib
import time
import csv


def pull_location(driver):

    cookies = driver.get_cookies()
    with open("./cookies.txt", "w", newline="\n", encoding="utf-8") as f:
        for cookie in cookies:

            f.write(cookie["name"] + " " + cookie["value"])
    # zip = ""
    # town_name = ""

    # zip = [cookie["value"] for cookie in cookies if cookie["name"] == "bcClubZipCode"]
    # town_name = [
    #     cookie["value"] for cookie in cookies if cookie["name"] == "bcClubName"
    # ]

    # print(" Type: " + str(type(zip)))
    # print("Zip code: ", zip )
    # print("Town: " + town_name)
    # print( " Type: " + type(town_name))
    # return zip, town_name


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

    # Testing variables
    tester = 0
    fake = 0

    for product in products:
        # Grabbing the HTML elements
        name_tag = product.select_one("div.product-tile__name")
        price_tag = product.select_one("span.base-price__regular > span")

        # Getting the text for the item
        name = name_tag.get_text(strip=True) if name_tag else "No name"
        price = price_tag.get_text(strip=True) if price_tag else "No price"

        # Just used for console level checking
        tester += 1
        if tester % 10 == 0:
            print("Product: " + name + " : " + price)

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

with open("./csv/store_data.csv", "w", newline="", encoding="utf-8") as f:
    zip_code, town = pull_location(driver)

    
    # address = zip_code + town
    # print("Address: " + address)
    # hashlib.md5(address.strip().lower().encode()).hexdigest()

    # f.write("id, street_address, zipcode")
    # f.write(address, town, zip_code)

time.sleep(10)
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
        parsing_status_done, product_count = pull_prods(
            soup, total_prods_int, product_count, writer
        )

        pg_count += 1
        soup = next_page(driver, pg_count, home_page)
        print("________________________________________________")


print("All products are pulled from this location")

driver.quit()
