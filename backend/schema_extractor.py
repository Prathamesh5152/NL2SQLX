# backend/schema_extractor.py
from sqlalchemy import inspect, text
from backend.db import engine
from backend.rag import rag_store
import pandas as pd

def extract_schema():
    """
    Returns schema dict and also pushes structured chunks into RAG.
    Schema dict format:
      { table_name: {"columns": [{"name":..., "type":...}, ...], "sample": [...] } }
    """
    inspector = inspect(engine)
    schema = {}
    # clear previous RAG entries (optional). If you want to preserve historic examples, remove this.
    rag_store.clear()

    tables = inspector.get_table_names()
    for table in tables:
        cols = inspector.get_columns(table)
        # sample rows (limit 5)
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

        # Create chunk text for this table
        col_lines = "\n".join([f"- {c['name']} ({c['type']})" for c in schema[table]["columns"]])
        sample_lines = ""
        if sample:
            # format a couple of sample rows as CSV-like lines
            sample_lines = "\nSample rows:\n"
            for row in sample:
                # show only first 3 columns to keep chunk small
                kv = ", ".join([f"{k}={v}" for k, v in list(row.items())[:6]])
                sample_lines += f"- {kv}\n"

        chunk = f"TABLE: {table}\nCOLUMNS:\n{col_lines}{sample_lines}"
        rag_store.add_chunk(chunk)

    # Optionally add an index-level chunk that describes relationships (FKs)
    # Add foreign keys info
    fk_chunks = []
    for table in tables:
        fks = inspector.get_foreign_keys(table)
        if fks:
            for fk in fks:
                ref = fk.get("referred_table")
                cols = fk.get("constrained_columns")
                fk_chunks.append(f"FK: {table}.{cols} -> {ref}")

    if fk_chunks:
        rag_store.add_chunks(fk_chunks)

    return schema
