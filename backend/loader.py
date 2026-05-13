from pypdf import PdfReader
import io


def load_file(path: str, content_bytes):
    """
    Konvertiert Nextcloud-Dateien in Text
    """

    # PDF
    if path.lower().endswith(".pdf"):
        reader = PdfReader(io.BytesIO(content_bytes))
        return "\n".join([page.extract_text() or "" for page in reader.pages])

    # Textdateien
    if path.lower().endswith((".txt", ".md", ".log")):
        if isinstance(content_bytes, bytes):
            return content_bytes.decode("utf-8", errors="ignore")
        return str(content_bytes)

    return None
