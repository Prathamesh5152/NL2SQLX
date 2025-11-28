# backend/schema_extractor.py

from sqlalchemy import inspect, text
from db import engine
from rag import add_schema_chunk, reset_rag_store


def extract_schema():
    """
    Extract the MySQL schema and push table descriptions into RAG.
    Returns schema dict:
      {
        table_name: {
            "columns": [...],
            "sample": [...]
        }
      }
    """
    inspector = inspect(engine)
    schema = {}

    # Reset/clear RAG store before adding new schema
    reset_rag_store()

    tables = inspector.get_table_names()

    for table in tables:
        # --- Extract columns ---
        cols = inspector.get_columns(table)

        # --- Extract sample rows ---
        sample = []
        try:
            with engine.connect() as conn:
                res = conn.execute(text(f"SELECT * FROM {table} LIMIT 5"))
                sample = [dict(r._mapping) for r in res]
        except Exception:
            sample = []

        schema[table] = {
            "columns": [{"name": c["name"], "type": str(c["type"])} for c in cols],
            "sample": sample
        }

        # --- Build RAG description chunk ---
        col_lines = "\n".join([
            f"- {c['name']} ({c['type']})"
            for c in schema[table]["columns"]
        ])

        sample_lines = ""
        if sample:
            sample_lines = "\nSample rows:\n"
            for row in sample:
                subset = ", ".join([
                    f"{k}={v}"
                    for k, v in list(row.items())[:6]
                ])
                sample_lines += f"- {subset}\n"

        chunk = (
            f"TABLE: {table}\n"
            f"COLUMNS:\n{col_lines}"
            f"{sample_lines}"
        )

        # --- Push chunk into RAG vector DB ---
        add_schema_chunk(table)

    # Return schema dict for API
    return schema
