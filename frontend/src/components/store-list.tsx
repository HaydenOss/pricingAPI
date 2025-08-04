"use client"

import React from 'react';

export async function getStores() {
    const stores = await fetch("http://127.0.0.1:8000/services/get-stores", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((res) => {
            if (!res.ok) throw new Error("Request failed");
            return res.json();
        })
        .then((data) => console.log("Store data:", data))
        .catch((err) => console.error("Store fetch error:", err));

    console.log("DATA: ", stores, " \n TYPE: ", typeof (stores));
    return { props: { stores } };
}

export default function StoreList({ stores }: { stores: string }) {


    return (
        <div>
            <p>{stores}</p>
        </div>
    );
}