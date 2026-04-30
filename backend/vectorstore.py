# simple in-memory store (für MVP)

store = []


def add_doc(text, meta):
    store.append({
        "text": text,
        "meta": meta
    })


def search(query):
    results = []

    for item in store:
        if query.lower() in item["text"].lower():
            results.append(item)

    return results
