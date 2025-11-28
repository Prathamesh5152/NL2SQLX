# backend/rag.py

from chromadb import Client
from chromadb.config import Settings

# Create in-memory ChromaDB store
client = Client(Settings(chroma_db_impl="duckdb+memory"))

# Create or reset schema collection
collection = client.get_or_create_collection("schema_chunks")

def reset_rag_store():
    """Clear all stored vectors before reloading schema."""
    try:
        client.delete_collection("schema_chunks")
    except:
        pass

    # Recreate empty collection
    global collection
    collection = client.create_collection("schema_chunks")

def add_schema_chunk(chunk_id: str, text: str):
    """Add a schema description to vector DB."""
    collection.add(
        ids=[chunk_id],
        documents=[text]
    )

def rag_search(query: str):
    """Return the closest schema text for the query."""
    result = collection.query(
        query_texts=[query],
        n_results=3
    )

    if (
        result and
        "documents" in result and
        result["documents"]
    ):
        docs = result["documents"][0]
        return "\n\n".join(docs)

    return ""
