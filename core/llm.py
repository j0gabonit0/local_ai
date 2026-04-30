import requests
import os

URL = os.getenv("OLLAMA_URL")


def ask_llm(prompt):

    r = requests.post(
        f"{URL}/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return r.json()["response"]
