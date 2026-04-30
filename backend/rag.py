from vectorstore import search


def build_context(query, groups):

    results = search(query)

    if not results:
        return "Kein Kontext gefunden."

    context = ""

    for r in results[:5]:
        context += f"\nSOURCE: {r['meta']}\nTEXT: {r['text']}\n"

    return context
