from sqlalchemy.sql import text
from db import engine

def run_sql(sql: str):
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = [dict(row._mapping) for row in result]
        return rows
