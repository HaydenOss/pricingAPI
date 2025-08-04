'use client'

import React from "react"

export default function Download() {

    function aldi_downloads() {
        fetch("http://127.0.0.1:8000/download/aldi", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then((res) => {
                if (!res.ok) throw new Error("Request failed");
                return res.json();
            })
            .then((data) => console.log("Aldi data:", data))
            .catch((err) => console.error("Aldi fetch error:", err));
    }

    function bjs_downloads() {
        fetch("http://127.0.0.1:8000/download/bjs", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then((res) => {
                if (!res.ok) throw new Error("Request failed");
                return res.json();
            })
            .then((data) => console.log("BJ's data:", data))
            .catch((err) => console.error("BJ's fetch error:", err));
    }

    return (

        <div className="flex flex-row gap-x-4 m-2">
            <button onClick={aldi_downloads}>
                Aldis
            </button>
            <button onClick={bjs_downloads}>
                Bj's
            </button>
        </div>

    );
}

