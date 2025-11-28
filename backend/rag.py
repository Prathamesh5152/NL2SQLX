from chromadb import Client
from chromadb.config import Settings

client = Client(Settings())
collection = client.get_or_create_collection("schema_vectors")


# ----------------------------
# FIX: reset store (new Chroma API)
# ----------------------------
def reset_rag_store():
    """
    Clears entire collection (Chroma v0.6+ compatible)
    """
    try:
        collection.delete(
            where={"$always": True}   # NEW FIX
        )
    except Exception:
        pass


def add_schema_chunk(text):
    """
    Add one schema chunk into vector store
    """
    collection.add(
        documents=[text],
        ids=[text[:50]]  # safe id
    )


def add_schema_chunks(chunks):
    """
    Add multiple schema chunks
    """
    for c in chunks:
        add_schema_chunk(c)


def rag_search(query, top_k=3):
    """
    vector search
    """
    try:
        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )

        if "documents" in results and results["documents"]:
            return results["documents"][0]

    except Exception as e:
        print("RAG search error:", e)

    return []
