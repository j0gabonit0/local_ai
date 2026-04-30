# simple persistent store mit verbesserter Suche

store = []


def add_doc(text, meta):
    store.append({
        "text": text,
        "meta": meta
    })


def search(query):
    results = []
    query_words = query.lower().split()

    for item in store:
        text_lower = item["text"].lower()
        # Match wenn IRGENDEIN Wort aus der Query im Text vorkommt
        if any(word in text_lower for word in query_words):
            results.append(item)

    return results


def get_store_size():
    return len(store)
