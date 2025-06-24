
from chromadb import PersistentClient
from chromadb.config import Settings
from memory.embedder import get_embedding
from typing import List, Dict
from config import CHROMADB_PATH
import uuid

class MemoryClient:
    def __init__(self, persist_directory=CHROMADB_PATH):
        # self.client = chromadb.Client(Settings(persist_directory=persist_directory))
        self.client = PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection("conversation_memory")

    def add_turn(self, speaker: str, message: str):
        embedding = get_embedding(message)
        self.collection.add(
            ids=[str(uuid.uuid4())],
            documents=[message],
            embeddings=[embedding],
            metadatas=[{"speaker": speaker}]
        )

    def query(self, query_text: str, n_results: int = 3) -> List[Dict]:
        embedding = get_embedding(query_text)
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=n_results
        )
        # Return matched documents and metadata
        return [
            {"message": doc, "speaker": meta["speaker"]}
            for doc, meta in zip(results["documents"][0], results["metadatas"][0])
        ]
