import React from "react";

function ResultPanel({ sql, result }) {
    return (
        <div className="card">
            {sql && (
                <>
                    <h3>Generated SQL</h3>
                    <pre className="sql-box">{sql}</pre>
                </>
            )}

            {result && (
                <>
                    <h3>Result</h3>
                    <pre className="result-box">
                        {JSON.stringify(result, null, 2)}
                    </pre>
                </>
            )}
        </div>
    );
}

export default ResultPanel;
