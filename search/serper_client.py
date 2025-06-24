import requests
from config import SERPER_API_KEY

def serper_search(query: str, num_results: int = 3):
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": query, "num": num_results}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data.get("organic", [])[:num_results]
    else:
        return []
