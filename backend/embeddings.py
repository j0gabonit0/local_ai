local_ai$ cat backend/embeddings.py 
import requests
import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")

def embed(text: str):
    r = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )
    return r.json()["embedding"]
sascha@sascha-tux:~/local_ai$ 
