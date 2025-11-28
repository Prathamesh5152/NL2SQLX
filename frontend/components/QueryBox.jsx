"use client"

import { useState } from "react"
import { Zap } from "lucide-react"

export default function QueryBox({ onQuery, loading }) {
  const [query, setQuery] = useState("")

  const handleSubmit = () => {
    onQuery(query)
  }

  return (
    <div className="card-modern">
      <div className="flex items-center gap-2 mb-4">
        <Zap className="w-5 h-5" style={{ color: "#6366f1" }} />
        <h3 className="text-lg font-semibold">Ask a Question</h3>
      </div>

      <textarea
        className="input-modern w-full h-28 mb-4"
        placeholder="Ask something about your data..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <button onClick={handleSubmit} disabled={loading} className="btn-primary disabled:opacity-50">
        {loading ? "Thinking…" : "Run Query"}
      </button>
    </div>
  )
}
