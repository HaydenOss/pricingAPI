import hashlib
import json
import csv


def store_file_mngmt(town: str, state: str, zip: str, store_name: str):
    with open("./store_numbers.json", "r", encoding="utf-8") as store_counter_file:
        data = json.load(store_counter_file)

        num_stores = data[store_name]
        num_stores += 1
        replacement_num = num_stores

        with open(
            "./csv/store_data.csv", "w", newline="", encoding="utf-8"
        ) as store_data_file:
            address = str(num_stores) + zip + town
            id = hashlib.md5(address.strip().lower().encode()).hexdigest()

            store_data_file.write("id, zip, state, town")
            store_data_file.write(id + "," + zip + "," + state + "," + town)

    with open(
        "./store_numbers.txt", "w", newline="", encoding="utf-8"
    ) as store_counter_file:
        store_counter_file.write(str(replacement_num))


def print_to_file_json(file_name, data):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=2)
