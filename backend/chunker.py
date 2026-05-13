def chunk_text(text: str, size: int = 800, overlap: int = 150):
    """
    Zerlegt Text in RAG-freundliche Chunks
    """

    chunks = []
    i = 0

    while i < len(text):
        chunks.append(text[i:i + size])
        i += size - overlap

    return chunks
