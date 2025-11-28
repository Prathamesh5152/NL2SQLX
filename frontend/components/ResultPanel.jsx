"use client"
import { Code, Table } from "lucide-react"

function ResultPanel({ sql, result }) {
  return (
    <div className="space-y-6">
      {sql && (
        <div className="card-modern">
          <div className="flex items-center gap-2 mb-4">
            <Code className="w-5 h-5" style={{ color: "#ec4899" }} />
            <h3 className="text-lg font-semibold">Generated SQL</h3>
          </div>
          <pre className="sql-box">{sql}</pre>
        </div>
      )}

      {result && result.length > 0 && (
        <div className="card-modern">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2">
              <Table className="w-5 h-5" style={{ color: "#10b981" }} />
              <h3 className="text-lg font-semibold">Query Results</h3>
              <span style={{ backgroundColor: "#334155", color: "#94a3b8" }} className="text-xs px-2 py-1 rounded">
                {result.length} rows
              </span>
            </div>
          </div>

          <div style={{ borderColor: "#334155" }} className="overflow-x-auto rounded-lg border">
            <table className="w-full text-sm">
              <thead>
                <tr style={{ backgroundColor: "#0f172a", borderBottomColor: "#475569", borderBottomWidth: "2px" }}>
                  {Object.keys(result[0]).map((col) => (
                    <th
                      key={col}
                      style={{ color: "#e2e8f0" }}
                      className="px-6 py-4 text-left font-semibold text-sm uppercase tracking-wider"
                    >
                      {col}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {result.map((row, i) => (
                  <tr
                    key={i}
                    style={{
                      borderBottomColor: "#334155",
                      backgroundColor: i % 2 === 0 ? "rgba(15, 23, 42, 0.4)" : "transparent",
                    }}
                    className="border-b transition-all duration-200 hover:bg-opacity-50"
                    onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "rgba(51, 65, 85, 0.3)")}
                    onMouseLeave={(e) =>
                      (e.currentTarget.style.backgroundColor = i % 2 === 0 ? "rgba(15, 23, 42, 0.4)" : "transparent")
                    }
                  >
                    {Object.values(row).map((val, j) => (
                      <td key={j} style={{ color: "#cbd5e1" }} className="px-6 py-4 whitespace-normal break-words">
                        {val !== null && val !== undefined ? (
                          <span style={{ color: "#e2e8f0" }}>
                            {typeof val === "number" ? val.toLocaleString() : String(val)}
                          </span>
                        ) : (
                          <span style={{ color: "#475569" }} className="italic">
                            null
                          </span>
                        )}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div style={{ color: "#94a3b8" }} className="mt-4 flex items-center justify-between text-xs">
            <span>
              Displaying {result.length} row{result.length !== 1 ? "s" : ""}
            </span>
            <span>
              {Object.keys(result[0]).length} column{Object.keys(result[0]).length !== 1 ? "s" : ""}
            </span>
          </div>
        </div>
      )}
    </div>
  )
}

export default ResultPanel
