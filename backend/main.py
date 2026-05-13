# ~/local_ai/backend/main.py

import os
import urllib3
import chromadb
import ollama

from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)

app = FastAPI()

CHROMA_PATH = os.getenv(
    "CHROMA_PATH",
    "/chroma_db"
)

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    "nextcloud_docs"
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# -----------------------------
# OPENAI MODEL LIST ENDPOINT
# -----------------------------

@app.get("/v1/models")
def models():

    return {
        "object": "list",
        "data": [
            {
                "id": "llama3",
                "object": "model",
                "owned_by": "local"
            }
        ]
    }


# -----------------------------
# OPENAI CHAT TYPES
# -----------------------------

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: list[Message]
    stream: bool = False


# -----------------------------
# CHAT ENDPOINT
# -----------------------------

@app.post("/v1/chat/completions")
def chat(req: ChatRequest):

    # letzte User Nachricht holen
    user_message = req.messages[-1].content

    print("\n==========================")
    print("USER QUESTION:")
    print(user_message)
    print("==========================\n")

    # Embedding erstellen
    query_embedding = embedding_model.encode(
        user_message
    ).tolist()

    # Chroma Suche
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    print("\n==========================")
    print("CHROMA RESULTS:")
    print(results)
    print("==========================\n")

    documents = results.get("documents", [])

    context = ""

    if documents and len(documents[0]) > 0:

        context = "\n\n".join(
            documents[0]
        )

    # Prompt bauen
    final_prompt = f"""
Du bist ein lokaler KI-Assistent mit Zugriff auf Nextcloud-Dokumente.

WICHTIGE REGELN:
- Nutze ausschließlich Informationen aus dem KONTEXT.
- Erfinde keine Informationen.
- Wenn Informationen fehlen, sage:
  'Keine Informationen im Nextcloud-Kontext gefunden.'
- Antworte auf Deutsch.
- Fasse Inhalte strukturiert zusammen.

KONTEXT:
-------------------------
{context}
-------------------------

FRAGE:
{user_message}

ANTWORT:
"""

    print("\n==========================")
    print("FINAL PROMPT:")
    print(final_prompt)
    print("==========================\n")

    # Ollama Anfrage
    response = ollama.chat(
        model=req.model,
        messages=[
            {
                "role": "user",
                "content": final_prompt
            }
        ]
    )

    answer = response["message"]["content"]

    print("\n==========================")
    print("OLLAMA ANSWER:")
    print(answer)
    print("==========================\n")

    # OpenAI kompatible Antwort
    return {
        "id": "local-rag",
        "object": "chat.completion",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": answer
                },
                "finish_reason": "stop"
            }
        ]
    }
