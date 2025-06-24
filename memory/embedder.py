from typing import List
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import OpenAIEmbeddings


embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# Returns a vector embedding for a given text

def get_embedding(text: str) -> List[float]:
    return embeddings.embed_query(text)
