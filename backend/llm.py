import requests

OLLAMA_URL = "http://ollama:11434"


def ask_llm(prompt):
    r = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return r.json().get("response", "")
