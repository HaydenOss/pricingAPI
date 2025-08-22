"use client";

import React, { useEffect, useState } from "react";

type Store = {
    store_id: number;
    store_name: string;
};



async function getStores() {
    try {
        const res = await fetch("http://127.0.0.1:8000/services/get-stores", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });
        if (!res.ok) throw new Error("Request failed");
        const data = await res.json();
        return data;
    } catch (err) {
        console.error("Store fetch error:", err);
        return [];
    }
}

export default function StoreList() {
    const baseLink = "http://localhost:3000";
    const [stores, setStores] = useState<Store[]>([]);

    useEffect(() => {
        const cachedStores = localStorage.getItem("stores");

        if (cachedStores) {
            setStores(JSON.parse(cachedStores));
        } else {
            getStores().then((res) => {
                if (!(res.status == 200)) throw new Error("Request failed");
                return res.data;
            })
                .then((obj) => {
                    setStores(obj.data);
                    localStorage.setItem("stores", JSON.stringify(obj.data));
                })
                .catch((err) => console.error("Store fetch error:", err));
        }
    }, []);

    return (
        <div className="">
            {stores.length === 0 ? (
                <p>No stores found.</p>
            ) : (
                <ul >
                    {stores.map((store: Store) => (
                        <li key={store.store_id} className="text-black hover:text-green-700 hover:underline "><a href= {baseLink + "/stores/" + store.store_name.toLowerCase()}>{store.store_name}</a></li>
                    ))}
                </ul>
            )}
        </div>
    );
}
