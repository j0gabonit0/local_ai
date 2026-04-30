from chromadb import Client

db = Client()
col = db.get_or_create_collection("docs")


def upsert_doc(text, metadata):
    col.add(
        documents=[text],
        metadatas=[metadata],
        ids=[metadata["path"]]
    )


def query_docs(query, groups):

    return col.query(
        query_texts=[query],
        n_results=5,
        where={"groups": {"$in": groups}}
    )
