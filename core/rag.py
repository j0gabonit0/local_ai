from core.index import query_docs
from core.llm import ask_llm


def answer(query, groups):

    docs = query_docs(query, groups)

    context = "\n".join(docs["documents"][0])

    prompt = f"""
Du bist ein Firmenassistent.

Nutze nur diesen Kontext:
{context}

Frage:
{query}
"""

    return ask_llm(prompt)
