# backend/rag.py
import os
import pickle
from typing import List
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

INDEX_PATH = os.path.join(os.path.dirname(__file__), "faiss_index.bin")
META_PATH = os.path.join(os.path.dirname(__file__), "faiss_meta.pkl")
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
EMBED_DIM = 384  # model embedding dim

class RAGStore:
    def __init__(self):
        self.model = SentenceTransformer(EMBED_MODEL_NAME)
        self.index = None
        self.metadata = []  # list[str] parallel to index vectors
        self._ensure_index_loaded()

    def _ensure_index_loaded(self):
        if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
            try:
                self.index = faiss.read_index(INDEX_PATH)
                with open(META_PATH, "rb") as f:
                    self.metadata = pickle.load(f)
                # sanity: ensure dims match
                if self.index.d != EMBED_DIM:
                    self._recreate_index()
            except Exception:
                self._recreate_index()
        else:
            self._recreate_index()

    def _recreate_index(self):
        self.index = faiss.IndexFlatL2(EMBED_DIM)
        self.metadata = []
        self.save()

    def add_chunk(self, text: str):
        """Add a single text chunk (schema or example) to index."""
        emb = self.model.encode([text], show_progress_bar=False)
        emb = np.array(emb, dtype="float32")
        self.index.add(emb)
        self.metadata.append(text)
        self.save()

    def add_chunks(self, texts: List[str]):
        if not texts:
            return
        embs = self.model.encode(texts, show_progress_bar=False)
        embs = np.array(embs, dtype="float32")
        self.index.add(embs)
        self.metadata.extend(texts)
        self.save()

    def search(self, query: str, top_k: int = 5) -> List[str]:
        """Return top_k text chunks relevant to query."""
        if self.index.ntotal == 0:
            return []
        q_emb = self.model.encode([query], show_progress_bar=False).astype("float32")
        distances, indices = self.index.search(q_emb, top_k)
        out = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                out.append(self.metadata[idx])
        return out

    def save(self):
        faiss.write_index(self.index, INDEX_PATH)
        with open(META_PATH, "wb") as f:
            pickle.dump(self.metadata, f)

    def clear(self):
        self._recreate_index()

# single global instance used by app
rag_store = RAGStore()
