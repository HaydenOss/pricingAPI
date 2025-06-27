from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import time

from pricing_api.src.scripts.file_management import print_to_file_json


def check_cookies():
    try:
        accept_btn = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        accept_btn.click()
        print("Accepted cookies.")
        time.sleep(1)
    except:
        print("No cookie popup found.")


def create_soup(link):
    # Open the page
    driver.get(link)
    time.sleep(2.5)
    check_cookies()
    return BeautifulSoup(driver.page_source, "html.parser")


def get_helper(key, container):
    if container:
        region_links = container.find_all("a", recursive=True)

        if key == 0:
            # for states
            for link in region_links:
                # Testing if each of the attributes exist
                try:
                    if link["href"]:
                        href = link["href"]
                    else:
                        continue

                    if link.find("span").text.strip():
                        name = link.find("span").text.strip()
                    else:
                        name = "NULL"

                    if link["data-count"][1:-1]:
                        count = link["data-count"][1:-1]
                    else:
                        count = -1
                except:
                    print("Error accessing key")

                # Creating the entry for each states's info
                new_link = home_page + href
                state_data[name] = {
                    "link": new_link,
                    "town_count": count,
                }
        else:
            # for towns
            tester = 3

            for link in region_links[3:]:
                tester += 1
                # Testing if each of the attributes exist
                try:
                    if link["href"]:
                        href = link["href"]
                    else:
                        continue

                    if link.find("span").text.strip():
                        name = link.find("span").text.strip()
                    else:
                        name = "NULL"

                    if link["data-count"][1:-1]:
                        count = int(link["data-count"][1:-1])
                    else:
                        count = -1
                except:
                    print("Error accessing key")

                if "towns" not in state_data[key]:
                    state_data[key]["towns"] = {}

                # Creating the entry for each town's info
                new_link = home_page + href
                state_data[key]["towns"][name] = {
                    "link": new_link,
                    "store_count": count,
                }
                print("New Link: " + new_link)
                # Getting the store addresses in each town and inserting into the dict
                if count == 1:
                    address_obj = get_single_address(new_link, 1)
                    state_data[key]["towns"][name]["stores"] = {1: address_obj}
                else:
                    address_obj = get_addresses(new_link)
                    state_data[key]["towns"][name]["stores"] = address_obj

                if tester % 5 == 0:
                    print(state_data)

    else:
        print("Could not access the state links properly")


def get_states():
    state_list_container = soup.select_one("#main > div.Main-content > section > div")
    get_helper(0, state_list_container)


def get_towns():
    for state, data in state_data.items():
        soup = create_soup(data["link"])

        town_list_container = soup.select_one(
            "#main > div.Main-content > section > div > ul"
        )

        get_helper(state, town_list_container)


def get_addresses(link):
    print(link)
    soup = create_soup(link)

    stores = {}
    links = []
    counter = 1

    # store_links = driver.find_elements(By.CLASS_NAME, "Teaser-titleWrapper")
    store_links = soup.select_one(
        "#main > div.Main-content > section > div > ul"
    ).find_all("a", recursive=True)

    for store in store_links:
        # opening the store address page
        if store["href"] and store["data-ya-track"] == "visitpage":

            single_address_link = store["href"]
            links.append(home_page + single_address_link[1:])

        else:
            print("Continuing to next in loop")
            print(store)
            continue


    for link in links:
        stores[counter] = get_single_address(link, counter)
        counter += 1

    return stores


def get_single_address(link, count):
    soup = create_soup(link)

    street_address = soup.select_one("#address > div:nth-child(1) > span").text.strip()
    zipcode = soup.select_one("#address > div:nth-child(3) > span").text.strip()
    print("Address: " + zipcode + " " + street_address)

    return {"street_address": street_address, "zipcode": zipcode}


home_page = "https://stores.aldi.us/"

options = Options()
# options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

print("________________________________________________")

soup = create_soup(home_page)

state_data = {}
get_states()
get_towns()

print_to_file_json("./data_files/stores/aldi_location_list.json", state_data)

print("________________________________________________")

driver.quit()
