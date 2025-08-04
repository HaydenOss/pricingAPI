// Dropdown.js
import React, { useState } from "react";
import FileUpload from "./file_upload";

export default function Dropdown() {
    const [dropdownOption, setDropdownOption] = useState("");
    const [selected, setSelected] = useState(false);

    const data_upload = (option: string) => {
        switch (option) {
            case "state":

                break;
            case "store":
                break;
            case "listings":
                break;
            case "products":
                break;
            default:
                break;
        }
    }

    const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        const option = event.target.value;
        setSelected(true)
        setDropdownOption(option);
        data_upload(option);


    }


    return (
        <div>
            <div>

                <select id="dropdown" value={dropdownOption} onChange={handleChange} className="">
                    <option value="">Choose Upload Option</option>
                    <option value="state">State</option>
                    <option value="store">Store</option>
                    <option value="listings">Listings</option>
                    <option value="products">Products</option>
                </select>
            </div>

            <div className={selected ? "visible" : "hidden"}>
                <FileUpload />
            </div>
        </div>
    );
}