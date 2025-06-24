import faiss
import numpy as np
from typing import List, Dict
from memory.embedder import get_embedding

class FaissMemoryClient:
    def __init__(self, dim=1536):
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []
        self.speakers = []

    def add_turn(self, speaker: str, message: str):
        embedding = np.array([get_embedding(message)], dtype='float32')
        self.index.add(embedding)
        self.texts.append(message)
        self.speakers.append(speaker)

    def query(self, query_text: str, n_results: int = 3) -> List[Dict]:
        if not self.texts:
            return []
        embedding = np.array([get_embedding(query_text)], dtype='float32')
        D, I = self.index.search(embedding, min(n_results, len(self.texts)))
        results = []
        for idx in I[0]:
            if idx < len(self.texts):
                results.append({"message": self.texts[idx], "speaker": self.speakers[idx]})
        return results 