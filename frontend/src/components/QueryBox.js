import React, { useState } from "react";
import { api } from "../api";

function QueryBox({ setSql, setResult }) {
    const [query, setQuery] = useState("");
    const [loading, setLoading] = useState(false);

    const runQuery = async () => {
        if (!query.trim()) return;

        setLoading(true);
        try {
            const res = await api.post("/query", null, {
                params: { user_input: query },
            });

            setSql(res.data.sql);
            setResult(res.data.result);
        } catch (err) {
            console.log(err);
            alert("Query failed");
        }
        setLoading(false);
    };

    return (
        <div className="card">
            <h2>Ask a Question</h2>

            <input
                type="text"
                placeholder="Ask something…"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
            />

            <button onClick={runQuery} disabled={loading}>
                {loading ? "Thinking…" : "Run"}
            </button>
        </div>
    );
}

export default QueryBox;
