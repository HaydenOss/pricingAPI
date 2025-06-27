from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import time
import csv

from pricing_api.src.scripts.file_management import store_file_mngmt


def cookie_popup():
    try:
        popup_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#onetrust-close-btn-container > button")
            )
        )
        popup_btn.click()
        print("Accepted cookies.")
        time.sleep(2)
    except:
        print("No cookie popup found.")


def get_location():
    # Opening the location page
    locator = driver.find_element(
        By.CSS_SELECTOR, "div.headerClubLocator.ml-2.only-desktop > span"
    )
    if locator:

        locator.click()
        time.sleep(1.5)
    else:
        print("Locator not found for location")

    # Pulling the location data
    location_div = driver.find_element(
        By.CSS_SELECTOR,
        "#stickyHeader_selectClub > div.address.pt-2.mt-4 > p:nth-child(3)",
    )

    if location_div:
        address = location_div.text
        add_split = address.split()
        print("Address: ", add_split)
    else:
        print("Location div not found.")

    return add_split[0], add_split[1], add_split[2]


# Parse all products
def get_prods(prod_count, writer):
    product_section = soup.select_one(
        "div.SearchResultsBlockstyle__SearchResultsStyle-sc-39c4cm-0.dQoxZn"
    )
    products = product_section.find_all(recursive=False)

    for product in products[prod_count:]:
        # Grabbing the HTML elements
        name = product.get("data-cnstrc-item-name")
        price = product.get("data-cnstrc-item-price")

        if not name:
            name = "NULL"
        if not price:
            price = "NULL"

        # Writing the text to the file
        writer.writerow([name, price, "Bj's"])
        prod_count += 1

    print(
        "Number of prods pulled so far: " + str(prod_count) + "/" + str(total_prods_int)
    )
    if total_prods_int != prod_count:
        return 0, prod_count
    else:
        print("Done pulling and saving prods")
        return 1, prod_count


def next_page(driver):
    try:
        load_more_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "#single-spa-application\:\@bjs\/plp-micro-frontend > main > div.SharedPlpViewstyle__SharedPLPOuterWrapper-sc-d5hmft-0.khyUHc > div.Commonstyles__SearchWrapper-sc-1ykuvkg-1.ikSGAP.is-grid-view > div.Loadmorestyle__LoadMoreStyle-sc-14fokh3-0.bkmoCh > button",
                )
            )
        )

        load_more_btn.click()
        print("Loading More Products")
        time.sleep(2)

        return BeautifulSoup(driver.page_source, "html.parser")
    except Exception as e:
        print("Could not click next page:", e)


home_page = "https://www.bjs.com/cg/grocery/?shopall=y&bcid=cghrba00&idt=20250204&icn=CLP_Grocery"

options = Options()
# options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

print("________________________________________________")
try:
    driver.get(home_page)
    time.sleep(0.5)
    cookie_popup()
    time.sleep(0.25)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    total_prods_item = soup.select_one(
        "#single-spa-application\:\@bjs\/plp-micro-frontend > main > div.SharedPlpViewstyle__SharedPLPOuterWrapper-sc-d5hmft-0.khyUHc > div.Commonstyles__SearchWrapper-sc-1ykuvkg-1.ikSGAP.is-grid-view > div.Loadmorestyle__LoadMoreStyle-sc-14fokh3-0.bkmoCh > p"
    )

    total_prods_arr = total_prods_item.get_text().split()
    print(total_prods_arr)
    total_prods = total_prods_arr[3]
    total_prods_int = int(total_prods)

    product_count = 0

    with open("./csv/bjs_products.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Product", "Price", "Store"])

        parsing_status_done = False

        while not parsing_status_done:
            parsing_status_done, product_count = get_prods(soup, writer)

            soup = next_page(driver)
            print("________________________________________________")
except:
    print("Error in opening page and pulling products")

town, state, zip = get_location()
store_file_mngmt(town, state, zip)
print("All products are pulled from this location")

driver.quit()
