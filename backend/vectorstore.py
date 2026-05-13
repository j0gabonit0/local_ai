import chromadb
from embeddings import embed

client = chromadb.PersistentClient(path="/chroma_db")
collection = client.get_or_create_collection("nextcloud_docs")


def add_doc(text, meta):
    vector = embed(text)

    collection.add(
        embeddings=[vector],
        documents=[text],
        metadatas=[meta],
        ids=[meta["id"]]
    )


def search(query, k=5):
    vector = embed(query)

    res = collection.query(
        query_embeddings=[vector],
        n_results=k
    )

    return [
        {
            "text": res["documents"][0][i],
            "meta": res["metadatas"][0][i]
        }
        for i in range(len(res["documents"][0]))
    ]
