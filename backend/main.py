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


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/index")
def index():
    return {"status": "ok"}


@app.post("/v1/chat/completions")
async def chat(req: Request):

    body = await req.json()
    messages = body.get("messages", [])

    query = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            query = m.get("content")
            break

    context = build_context(query)

    print("\n===== CONTEXT DEBUG =====")
    print(context)
    print("========================\n")

    prompt = f"""
Du bist ein Firmenassistent.

Nutze nur diesen Kontext:
{context}

Frage: {query}
"""

    answer = ask_llm(prompt)

    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": answer
                }
            }
        ]
    }
