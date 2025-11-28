# backend/rag.py

from chromadb import PersistentClient

# Use an in-memory temporary folder at runtime
client = PersistentClient(path="/tmp/chroma-db")

# Create / Get collection
collection = client.get_or_create_collection("schema_chunks")


def reset_rag_store():
    """Clear the existing schema collection."""
    global collection
    try:
        client.delete_collection("schema_chunks")
    except:
        pass

    collection = client.get_or_create_collection("schema_chunks")


def add_schema_chunk(chunk_id: str, text: str):
    """Insert schema text chunk into vector DB."""
    collection.add(
        ids=[chunk_id],
        documents=[text]
    )


def rag_search(query: str):
    """Retrieve relevant schema chunks."""
    result = collection.query(
        query_texts=[query],
        n_results=3
    )

    docs = result.get("documents", [[]])[0]

    if docs:
        return "\n\n".join(docs)

    return ""
