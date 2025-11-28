"use client"

import { useState } from "react"
import axios from "axios"
import { Github, Linkedin } from "lucide-react"
import UploadCSV from "@/components/UploadCSV"
import QueryBox from "@/components/QueryBox"
import ResultPanel from "@/components/ResultPanel"

const API_BASE = "https://nl2sqlx.onrender.com"

export default function App() {
  const [csvMessage, setCsvMessage] = useState("")
  const [sql, setSql] = useState("")
  const [result, setResult] = useState([])
  const [loading, setLoading] = useState(false)

  // ===============================
  // 1. UPLOAD CSV
  // ===============================
  const handleCSVUpload = async (file) => {
    const formData = new FormData()
    formData.append("file", file)

    try {
      const res = await axios.post(`${API_BASE}/upload-csv`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      setCsvMessage(`Uploaded: ${res.data.table_created} (${res.data.rows_inserted} rows)`)
    } catch (err) {
      setCsvMessage("Upload failed.")
      console.error(err)
    }
  }

  // ===============================
  // 2. RUN NL → SQL QUERY
  // ===============================
  const handleRunQuery = async (prompt) => {
    if (!prompt.trim()) return
    setLoading(true)

    try {
      const res = await axios.post(`${API_BASE}/query`, null, {
        params: { user_input: prompt },
      })
      setSql(res.data.sql)
      setResult(res.data.result || [])
    } catch (err) {
      console.error(err)
      setSql("ERROR: " + (err.response?.data?.error || "Unknown error"))
    }
    setLoading(false)
  }

  // ===============================
  // 3. FINISH — DELETE TEMP TABLES
  // ===============================
  const handleFinish = async () => {
    try {
      const res = await axios.post(`${API_BASE}/finish`)
      alert(res.data.message)
      setCsvMessage("")
      setSql("")
      setResult([])
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div style={{ minHeight: "100vh", backgroundColor: "#0f172a", color: "#f1f5f9" }}>
      <header
        style={{ borderBottomColor: "#334155", borderBottomWidth: "1px" }}
        className="sticky top-0 z-50 backdrop-blur-md"
      >
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1
              className="text-3xl font-bold"
              style={{
                background: "linear-gradient(to right, #6366f1, #ec4899)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
              }}
            >
              NL2SQLX
            </h1>
            <p style={{ color: "#cbd5e1" }} className="text-sm">
              Learn SQL by Asking Questions
            </p>
          </div>

          {/* Social Links */}
          <div className="flex items-center gap-4">
            <a
              href="https://github.com/Prathamesh5152"
              target="_blank"
              rel="noopener noreferrer"
              className="transition-transform duration-300 hover:scale-110"
              style={{
                padding: "8px 12px",
                borderRadius: "8px",
                background: "linear-gradient(to right, #1e40af, #0369a1)",
              }}
            >
              <Github className="w-5 h-5" style={{ color: "#ffffff" }} />
            </a>
            <a
              href="https://www.linkedin.com/in/prathameshsalokhe/"
              target="_blank"
              rel="noopener noreferrer"
              className="transition-transform duration-300 hover:scale-110"
              style={{
                padding: "8px 12px",
                borderRadius: "8px",
                background: "linear-gradient(to right, #06b6d4, #00d9ff)",
              }}
            >
              <Linkedin className="w-5 h-5" style={{ color: "#ffffff" }} />
            </a>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-12">
        {/* Hero section */}
        <div className="mb-12">
          <p style={{ color: "#cbd5e1" }} className="text-lg leading-relaxed max-w-2xl">
            Upload your own dataset and let AI convert your questions into SQL. See the generated query and results
            instantly.
          </p>
        </div>

        {/* Upload CSV Component */}
        <UploadCSV onUpload={handleCSVUpload} message={csvMessage} />

        {csvMessage && (
          <div className="space-y-8 mt-8">
            {/* Query Box Component */}
            <QueryBox onQuery={handleRunQuery} loading={loading} />

            {/* Result Panel Component */}
            <ResultPanel sql={sql} result={result} />

            <div className="flex justify-end">
              <button onClick={handleFinish} className="btn-danger">
                Finish & Delete Temporary Data
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
