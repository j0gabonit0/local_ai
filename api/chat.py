from fastapi import APIRouter
from core.auth import get_groups
from core.rag import answer

router = APIRouter()


@router.post("/chat")
def chat(req: dict):

    groups = get_groups(req["user"], req["password"])

    return {
        "answer": answer(req["query"], groups)
    }
