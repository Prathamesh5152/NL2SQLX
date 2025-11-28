from chromadb import Client
from chromadb.config import Settings
import numpy as np

client = Client(Settings())
collection = client.get_or_create_collection("schema_vectors")

def reset_rag_store():
    collection.delete(where={})

def add_schema_chunk(text):
    collection.add(
        documents=[text],
        ids=[str(np.random.randint(1e12))]
    )

def rag_search(query, top_k=3):   # 👈 FIXED HERE
    """
    Return top_k relevant schema chunks.
    """
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    if "documents" in results and results["documents"]:
        return results["documents"][0]
    return []
