from vectorstore import search


def build_context(query, groups=None):

    results = search(query)

    if not results:
        return ""

    context = ""

    for r in results:
        context += f"\nSOURCE: {r['meta']}\nTEXT: {r['text']}\n"

    return context
