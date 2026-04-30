from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

store = []


def add_doc(text, meta):
    emb = model.encode(text)

    store.append({
        "text": text,
        "meta": meta,
        "embedding": emb
    })


def search(query, top_k=5):
    q_emb = model.encode(query)

    scores = []

    for item in store:
        score = np.dot(q_emb, item["embedding"])
        scores.append((score, item))

    scores.sort(reverse=True, key=lambda x: x[0])

    return [x[1] for x in scores[:top_k]]
