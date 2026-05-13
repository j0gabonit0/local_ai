from chroma_store import search

def build_context(query, collection=None, k=5):
    results = search(query, k=k)

    docs = results.get("documents", [[]])[0]

    if not docs:
        return ""

    return "\n\n".join(docs)
