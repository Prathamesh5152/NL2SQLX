from fastapi import FastAPI, UploadFile, File
from schema_extractor import extract_schema
from validator import clean_sql, is_safe_sql, ensure_groupby_safe

from sql_runner import run_sql
from nl2sql import generate_sql
from db import engine  # <-- ADD THIS
import pandas as pd
from sqlalchemy import text
from schema_extractor import extract_schema
from nl2sql import generate_sql
from sql_runner import run_sql
from db import engine
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# if not already: rag_store is used inside schema_extractor through extract_schema()




# app = FastAPI

SCHEMA = extract_schema()

@app.get("/")
def home():
    return {"message": "AI SQL Framework Running!"}


@app.post("/upload-csv")
def upload_csv(file: UploadFile = File(...)):

    # Read CSV into pandas
    df = pd.read_csv(file.file)

    # Extract table name
    table_name = file.filename.split(".")[0]

    # Insert into MySQL
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)

    # Refresh schema
    global SCHEMA
    SCHEMA = extract_schema()
    UPLOADED_TABLES.append(table_name)

    return {
        "status": "success",
        "message": f"Table '{table_name}' uploaded successfully!",
        "rows_inserted": len(df),
        "table_created": table_name,
        "columns": df.columns.tolist()
    }


@app.post("/query")
def query_ai(user_input: str):
    try:
        # Generate SQL using LLM + RAG context + validation
        sql = generate_sql(user_input, SCHEMA)

        # Run SQL
        result = run_sql(sql)

        return {
            "user_input": user_input,
            "sql": sql,
            "result": result
        }
    except Exception as e:
        return {"error": str(e)}

    # @app.post("/query")
    # def query_ai(user_input: str):

    #     # Hard-coded test SQL (no AI)
    #     sql = "SELECT 1 AS test_value;"

    #     result = run_sql(sql)

    #     return {
    #         "input": user_input,
    #         "sql": sql,
    #         "result": result
    #     }
UPLOADED_TABLES = []


@app.on_event("shutdown")
def cleanup_tables():
    print("🔥 Cleaning up uploaded tables...")

    with engine.connect() as conn:
        for table in UPLOADED_TABLES:
            try:
                conn.execute(text(f"DROP TABLE IF EXISTS {table}"))
                print(f"Deleted table: {table}")
            except Exception as e:
                print("Error deleting table:", table, e)

@app.post("/finish")
def finish_session():
    """
    Delete all uploaded tables immediately when user clicks Finish.
    """
    global UPLOADED_TABLES
    try:
        with engine.connect() as conn:
            for table in UPLOADED_TABLES:
                conn.execute(text(f"DROP TABLE IF EXISTS {table}"))
                print("Deleted table:", table)

            conn.commit()

        # Reset local memory
        UPLOADED_TABLES = []
        global SCHEMA
        SCHEMA = extract_schema()

        return {"status": "success", "message": "User session finished. All tables deleted."}

    except Exception as e:
        return {"status": "error", "message": str(e)}
    

@app.get("/")
def home():
    return {"status": "Backend running", "cors": "enabled"}

