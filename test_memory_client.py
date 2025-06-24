from memory.memory_client import MemoryClient

client = MemoryClient()
client.add_turn("user", "This is a test message.")
results = client.query("test")

print("Query Results:", results)