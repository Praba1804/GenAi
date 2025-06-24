from chromadb import PersistentClient

client = PersistentClient(path="./chroma_test_db")  # 👈 updated initialization
collection = client.get_or_create_collection("test_collection")

collection.add(
    ids=["1"],
    documents=["Hello world!"],
    embeddings=[[0.0]*1536],  # Dummy embedding for ada-002
    metadatas=[{"speaker": "user"}]
)

results = collection.query(
    query_embeddings=[[0.0]*1536],
    n_results=1
)

print("ChromaDB test passed. Results:", results)
