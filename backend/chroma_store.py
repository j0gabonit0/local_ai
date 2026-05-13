import chromadb
import os

DB_PATH = os.getenv("CHROMA_PATH", "/chroma_db")

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection("memory")


def add_doc(text, metadata=None):
    collection.add(
        documents=[text],
        metadatas=[metadata or {}],
        ids=[str(hash(text))]
    )


def search(query, k=5):
    return collection.query(
        query_texts=[query],
        n_results=k
    )
