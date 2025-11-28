"use client"

import { Upload } from "lucide-react"

export default function UploadCSV({ onUpload, message }) {
  const handleChange = (e) => {
    const file = e.target.files?.[0]
    if (file) onUpload(file)
  }

  return (
    <div className="card-modern">
      <div className="flex items-center gap-2 mb-4">
        <Upload className="w-5 h-5" style={{ color: "#f59e0b" }} />
        <h3 className="text-lg font-semibold">Upload CSV File</h3>
      </div>

      <input type="file" accept=".csv" onChange={handleChange} className="input-modern w-full cursor-pointer" />

      {message && (
        <p style={{ color: "#10b981" }} className="mt-4 text-sm">
          {message}
        </p>
      )}
    </div>
  )
}
