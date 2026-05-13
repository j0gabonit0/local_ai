# ~/local_ai/backend/main.py

import os
import urllib3
import chromadb
import ollama

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

# SSL Warnings deaktivieren
urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)

# FastAPI App
app = FastAPI()

# ---------------------------------------------------
# ENV
# ---------------------------------------------------

CHROMA_PATH = os.getenv(
    "CHROMA_PATH",
    "/chroma_db"
)

OLLAMA_HOST = os.getenv(
    "OLLAMA_URL",
    "http://ollama:11434"
)

# ---------------------------------------------------
# OLLAMA CLIENT
# ---------------------------------------------------

ollama_client = ollama.Client(
    host=OLLAMA_HOST
)

# ---------------------------------------------------
# CHROMA
# ---------------------------------------------------

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    "nextcloud_docs"
)

# ---------------------------------------------------
# EMBEDDING MODEL
# ---------------------------------------------------

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# ---------------------------------------------------
# OPENAI MODEL ENDPOINT
# ---------------------------------------------------

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

# ---------------------------------------------------
# OPENAI TYPES
# ---------------------------------------------------

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: list[Message]
    stream: bool = False

# ---------------------------------------------------
# CHAT ENDPOINT
# ---------------------------------------------------

@app.post("/v1/chat/completions")
def chat(req: ChatRequest):

    try:

        # -------------------------------------------
        # USER MESSAGE
        # -------------------------------------------

        user_message = req.messages[-1].content

        print("\n==========================")
        print("USER QUESTION:")
        print(user_message)
        print("==========================\n")

        # -------------------------------------------
        # EMBEDDING
        # -------------------------------------------

        query_embedding = embedding_model.encode(
            user_message
        ).tolist()

        # -------------------------------------------
        # CHROMA QUERY
        # -------------------------------------------

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5
        )

        print("\n==========================")
        print("CHROMA RESULTS:")
        print(results)
        print("==========================\n")

        documents = results.get(
            "documents",
            []
        )

        context = ""

        if documents and len(documents[0]) > 0:

            context = "\n\n".join(
                documents[0]
            )

        # -------------------------------------------
        # FINAL PROMPT
        # -------------------------------------------

        final_prompt = f"""
Du bist ein lokaler KI-Assistent mit Zugriff auf Nextcloud-Dokumente.

WICHTIGE REGELN:
- Nutze ausschließlich Informationen aus dem KONTEXT
- Erfinde keine Informationen
- Wenn nichts gefunden wird sage:
  'Keine Informationen im Nextcloud-Kontext gefunden.'
- Antworte auf Deutsch
- Fasse Inhalte strukturiert zusammen

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

        # -------------------------------------------
        # OLLAMA
        # -------------------------------------------

        response = ollama_client.chat(
            model=req.model,
            messages=[
                {
                    "role": "user",
                    "content": final_prompt
                }
            ]
        )

        print("\n==========================")
        print("OLLAMA RESPONSE:")
        print(response)
        print("==========================\n")

        answer = response["message"]["content"]

        # -------------------------------------------
        # OPENAI RESPONSE
        # -------------------------------------------

        return JSONResponse(
            content={
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
        )

    except Exception as e:

        print("\n==========================")
        print("ERROR:")
        print(str(e))
        print("==========================\n")

        return JSONResponse(
            status_code=500,
            content={
                "error": str(e)
            }
        )
