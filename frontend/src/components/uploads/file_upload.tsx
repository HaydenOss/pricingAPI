import React, { useState } from "react";

export default function FileUpload() {
    const [file, setFile] = useState();

    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files[0]) {
            setFile(event.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch("http://localhost:3000/upload", {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        console.log(result);
    };

    return (
        <div>
            <input className="border-2 border-blue-500 px-4 py-2 text-blue-500" type="file" onChange={handleChange} />
            <button className="border-2 border-blue-500 px-4 py-2 text-blue-500" onClick={handleUpload}>Upload</button>
        </div>
    );
};
