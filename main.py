from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from rag import build_context
from llm import ask_llm

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# ROOT
# -------------------------
@app.get("/")
def root():
    return {"status": "ok"}


# -------------------------
# INDEX TEST
# -------------------------
@app.get("/index")
def index():
    return {"status": "ok"}


# -------------------------
# OPENAI COMPATIBLE CHAT ENDPOINT
# -------------------------
@app.post("/v1/chat/completions")
async def chat(req: Request):

    body = await req.json()
    messages = body.get("messages", [])

    # letzte User Message extrahieren
    query = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            query = m.get("content")
            break

    if not query:
        return {
            "error": "no user message found"
        }

    # RAG CONTEXT BUILD
    context = build_context(query)

    # DEBUG OUTPUT
    print("\n===== CONTEXT DEBUG =====")
    print("QUERY:", query)
    print("CONTEXT:\n", context)
    print("========================\n")

    # Prompt bauen
    prompt = f"""
Du bist ein Firmenassistent.

Nutze nur diesen Kontext:

{context}

Frage: {query}
"""

    # LLM CALL
    try:
        answer = ask_llm(prompt)
    except Exception as e:
        return {
            "error": "llm_error",
            "details": str(e)
        }

    # OpenAI kompatible Response
    return {
        "id": "chatcmpl-local",
        "object": "chat.completion",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": answer
                }
            }
        ]
    }
