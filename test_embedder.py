from memory.embedder import get_embedding

embedding = get_embedding("This is a test message.")
print("Embedding length:", len(embedding))