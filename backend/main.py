from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

from indexer import index_nextcloud
from rag import build_context

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://ollama:11434"


# ----------------------------
# HEALTH
# ----------------------------
@app.get("/")
def root():
    return {"status": "Nextcloud AI läuft"}


# ----------------------------
# INDEX NEXTCLOUD
# ----------------------------
@app.get("/index")
def index():

    result = index_nextcloud()

    return {
        "status": "ok",
        "files_found": result.get("files", 0),
        "documents_indexed": result.get("count", 0)
    }


# ----------------------------
# CHAT (RAG)
# ----------------------------
@app.post("/chat")
def chat(req: dict):

    query = req.get("query")
    user = req.get("user", "unknown")

    if not query:
        return {"error": "query fehlt"}

    groups = ["HR", "Finance"]

    context = build_context(query, groups)

    prompt = f"""
Du bist ein Firmenassistent.

Nutze ausschließlich diesen Kontext:

{context}

Frage: {query}
"""

    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": "llama3:latest",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        data = r.json()

        return {
            "answer": data.get("response", ""),
            "user": user
        }

    except Exception as e:
        return {
            "error": "LLM Fehler",
            "details": str(e)
        }
