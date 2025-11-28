# backend/nl2sql.py
import os
from dotenv import load_dotenv
from groq import Groq
from rag import rag_search


from validator import clean_sql, is_safe_sql, ensure_groupby_safe

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# LLM model to use (replace if your Groq account needs another)
GROQ_MODEL = "openai/gpt-oss-120b"

def build_prompt(user_query: str, retrieved_chunks: list, schema_snapshot: dict) -> str:
    """
    Builds a strict prompt for NL -> SQL using retrieved RAG chunks + a compact schema snapshot.
    `schema_snapshot` is the output of extract_schema() so we can include a minimal table/cols map.
    """
    # compact schema summary
    schema_lines = []
    for table, info in schema_snapshot.items():
        cols = ", ".join([c["name"] for c in info["columns"]])
        schema_lines.append(f"{table}({cols})")
    schema_summary = "\n".join(schema_lines)

    # join retrieved context (RAG)
    context = "\n\n".join(retrieved_chunks) if retrieved_chunks else "No additional context found."

    prompt = f"""
You are a SQL expert. Generate a VALID MySQL query for the user's request.

STRICT RULES:
1) OUTPUT ONLY a single SQL query, no explanation, no markdown, no backticks.
2) Use ONLY tables and columns available in the SCHEMA SUMMARY below or in the CONTEXT chunks below.
3) NEVER hallucinate columns or tables.
4) If aggregation is required, use appropriate aggregate functions (SUM, COUNT, AVG, MIN, MAX).
5) If GROUP BY is used, ensure all non-grouped columns are aggregated.
6) For revenue or totals ALWAYS use SUM(quantity_column * price_column) (replace names with columns present).
7) Do not use SELECT * unless user explicitly asked for all columns.
8) Do not modify or drop tables.

SCHEMA SUMMARY:
{schema_summary}

RETRIEVED CONTEXT (most relevant chunks):
{context}

USER REQUEST:
{user_query}

Return only the SQL query.
"""
    return prompt

def generate_sql(user_query: str, schema_snapshot: dict, top_k: int = 6) -> str:
    """
    1) Use RAG to retrieve top-k schema chunks relevant to the user query
    2) Build a strict prompt + schema snapshot
    3) Call Groq LLM
    4) Clean and validate SQL
    """
    # 1. retrieve
    retrieved = rag_search(user_query, top_k=top_k)

    # 2. prompt
    prompt = build_prompt(user_query, retrieved, schema_snapshot)

    # 3. call LLM (wrap exceptions)
    try:
        resp = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=512
        )
        raw_sql = resp.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"LLM error: {e}")

    sql = clean_sql(raw_sql)

    # 4. validation
    safe, msg = is_safe_sql(sql)
    if not safe:
        raise RuntimeError(f"Unsafe SQL blocked: {msg}")

    group_ok, gmsg = ensure_groupby_safe(sql)
    if not group_ok:
        # attempt to repair simple revenue/group by intent by adding SUM if pattern matches
        # but safer to refuse — we'll throw an error back so frontend/user can refine question
        raise RuntimeError(f"GROUP BY validation failed: {gmsg}")

    # final sanity: make sure query uses only schema names (simple check)
    # optionally add more checks here

    return sql
