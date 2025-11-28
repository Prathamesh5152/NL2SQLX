import React, { useState } from "react";
import axios from "axios";

const API_BASE = "http://localhost:8000";

function App() {
  const [csvMessage, setCsvMessage] = useState("");
  const [prompt, setPrompt] = useState("");
  const [sqlOutput, setSqlOutput] = useState("");
  const [result, setResult] = useState([]);
  const [loading, setLoading] = useState(false);

  // ===============================
  // 1. UPLOAD CSV
  // ===============================
  const handleCSVUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(`${API_BASE}/upload-csv`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });

      setCsvMessage(`Uploaded: ${res.data.table_created} (${res.data.rows_inserted} rows)`);

    } catch (err) {
      setCsvMessage("Upload failed.");
      console.error(err);
    }
  };

  // ===============================
  // 2. RUN NL → SQL QUERY
  // ===============================
  const runQuery = async () => {
    if (!prompt.trim()) return;
    setLoading(true);

    try {
      const res = await axios.post(`${API_BASE}/query`, null, {
        params: { user_input: prompt }
      });

      setSqlOutput(res.data.sql);
      setResult(res.data.result || []);

    } catch (err) {
      console.error(err);
      setSqlOutput("ERROR: " + (err.response?.data?.error || "Unknown error"));
    }

    setLoading(false);
  };

  // ===============================
  // 3. FINISH — DELETE TEMP TABLES
  // ===============================
  const finishSession = async () => {
    const res = await axios.post(`${API_BASE}/finish`);
    alert(res.data.message);

    setCsvMessage("");
    setPrompt("");
    setSqlOutput("");
    setResult([]);
  };

  return (
    <div style={styles.container}>

      <h1>NL2SQLX Dashboard</h1>

      {/* UPLOAD CSV */}
      <div style={styles.card}>
        <h3>Upload CSV File</h3>
        <input type="file" accept=".csv" onChange={handleCSVUpload} />
        <p>{csvMessage}</p>
      </div>

      {/* QUERY BOX */}
      <div style={styles.card}>
        <h3>Ask Anything in Natural Language</h3>
        <textarea
          style={styles.textarea}
          placeholder="Example: Show total revenue by category..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        <button onClick={runQuery} style={styles.button}>
          {loading ? "Processing..." : "Run Query"}
        </button>
      </div>

      {/* SQL OUTPUT */}
      {sqlOutput && (
        <div style={styles.card}>
          <h3>Generated SQL</h3>
          <pre style={styles.codeBox}>{sqlOutput}</pre>
        </div>
      )}

      {/* RESULT TABLE */}
      {result.length > 0 && (
        <div style={styles.card}>
          <h3>Query Result</h3>

          <table style={styles.table}>
            <thead>
              <tr>
                {Object.keys(result[0]).map((col) => (
                  <th key={col}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {result.map((row, i) => (
                <tr key={i}>
                  {Object.values(row).map((val, j) => (
                    <td key={j}>{val}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* FINISH SESSION */}
      <button onClick={finishSession} style={styles.dangerButton}>
        Finish & Delete Temporary Data
      </button>
    </div>
  );
}

// SIMPLE UI STYLES
const styles = {
  container: {
    padding: "40px",
    maxWidth: "900px",
    margin: "auto",
    fontFamily: "Arial"
  },
  card: {
    padding: "20px",
    border: "1px solid #ddd",
    borderRadius: "10px",
    marginBottom: "25px",
    backgroundColor: "#fafafa"
  },
  textarea: {
    width: "100%",
    height: "100px",
    padding: "10px",
    fontSize: "16px"
  },
  button: {
    padding: "10px 20px",
    marginTop: "10px",
    backgroundColor: "#007bff",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer"
  },
  dangerButton: {
    padding: "12px 20px",
    backgroundColor: "#dc3545",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
    fontSize: "16px"
  },
  codeBox: {
    padding: "15px",
    background: "#272822",
    color: "white",
    borderRadius: "8px"
  },
  table: {
    width: "100%",
    borderCollapse: "collapse"
  }
};

export default App;
