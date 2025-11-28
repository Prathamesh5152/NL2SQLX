import React, { useState } from "react";
import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export default function UploadCSV() {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState("");
    const [error, setError] = useState(false);

    const handleUpload = async () => {
        if (!file) {
            setMessage("Please select a CSV file");
            setError(true);
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            const res = await axios.post(`${API_BASE}/upload-csv`, formData, {
                headers: { "Content-Type": "multipart/form-data" }
            });

            if (res.status === 200) {
                setMessage(res.data.message || "Upload successful");
                setError(false);
            } else {
                setMessage("Upload failed");
                setError(true);
            }
        } catch (err) {
            console.error("Upload error:", err);
            setMessage("Upload failed");
            setError(true);
        }
    };

    return (
        <div style={{ padding: "40px", textAlign: "center" }}>
            <h1>NL2SQLX Learning Platform</h1>

            <div
                style={{
                    width: "60%",
                    margin: "20px auto",
                    padding: "30px",
                    borderRadius: "12px",
                    boxShadow: "0 2px 10px rgba(0,0,0,0.15)",
                    background: "white"
                }}
            >
                <h2>Upload a CSV File</h2>

                {/* File Picker */}
                <input
                    type="file"
                    accept=".csv"
                    onChange={(e) => setFile(e.target.files[0])}
                    style={{ marginTop: "20px" }}
                />

                {/* Upload Button */}
                <div style={{ marginTop: "20px" }}>
                    <button
                        onClick={handleUpload}
                        style={{
                            background: "#007BFF",
                            color: "white",
                            border: "none",
                            padding: "10px 20px",
                            borderRadius: "6px",
                            cursor: "pointer",
                        }}
                    >
                        Upload
                    </button>
                </div>

                {/* Message */}
                {message && (
                    <p
                        style={{
                            marginTop: "15px",
                            color: error ? "red" : "green",
                            fontWeight: "bold",
                        }}
                    >
                        {message}
                    </p>
                )}
            </div>
        </div>
    );
}
