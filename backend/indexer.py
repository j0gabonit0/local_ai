import os
import tempfile
import requests
import chromadb
import urllib3

from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from docx import Document

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)

NEXTCLOUD_URL = os.getenv("NEXTCLOUD_URL")
NEXTCLOUD_USER = os.getenv("NEXTCLOUD_USER")
NEXTCLOUD_PASS = os.getenv("NEXTCLOUD_PASS")

CHROMA_PATH = os.getenv(
    "CHROMA_PATH",
    "/chroma_db"
)

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    "nextcloud_docs"
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

WEBDAV_URL = (
    f"{NEXTCLOUD_URL}/remote.php/dav/files/"
    f"{NEXTCLOUD_USER}/"
)


def get_nextcloud_files():

    response = requests.request(
        "PROPFIND",
        WEBDAV_URL,
        auth=(
            NEXTCLOUD_USER,
            NEXTCLOUD_PASS
        ),
        headers={
            "Depth": "infinity"
        },
        verify=False
    )

    soup = BeautifulSoup(
        response.text,
        "xml"
    )

    files = []

    for href in soup.find_all("d:href"):

        file_path = href.text

        if (
            file_path.endswith(".txt")
            or file_path.endswith(".md")
            or file_path.endswith(".pdf")
            or file_path.endswith(".docx")
        ):
            files.append(file_path)

    return files


def download_file(file_path):

    file_url = f"{NEXTCLOUD_URL}{file_path}"

    response = requests.get(
        file_url,
        auth=(
            NEXTCLOUD_USER,
            NEXTCLOUD_PASS
        ),
        verify=False
    )

    return response.content


def extract_text(file_path, content):

    if file_path.endswith(".txt"):

        return content.decode("utf-8")

    if file_path.endswith(".md"):

        return content.decode("utf-8")

    if file_path.endswith(".pdf"):

        with tempfile.NamedTemporaryFile(
            suffix=".pdf"
        ) as tmp:

            tmp.write(content)
            tmp.flush()

            reader = PdfReader(tmp.name)

            text = ""

            for page in reader.pages:

                extracted = page.extract_text()

                if extracted:
                    text += extracted

            return text

    if file_path.endswith(".docx"):

        with tempfile.NamedTemporaryFile(
            suffix=".docx"
        ) as tmp:

            tmp.write(content)
            tmp.flush()

            doc = Document(tmp.name)

            return "\n".join(
                [p.text for p in doc.paragraphs]
            )

    return ""


def split_text(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):

        chunks.append(
            text[i:i + chunk_size]
        )

    return chunks


def index_documents():

    files = get_nextcloud_files()

    print(f"Found {len(files)} files")

    for file_path in files:

        try:

            print(f"Indexing {file_path}")

            binary_content = download_file(
                file_path
            )

            text = extract_text(
                file_path,
                binary_content
            )

            if not text.strip():

                print(
                    f"No text extracted: {file_path}"
                )

                continue

            chunks = split_text(text)

            for idx, chunk in enumerate(chunks):

                embedding = embedding_model.encode(
                    chunk
                ).tolist()

                collection.add(
                    ids=[
                        f"{file_path}_{idx}"
                    ],
                    documents=[chunk],
                    embeddings=[embedding],
                    metadatas=[{
                        "owner": NEXTCLOUD_USER,
                        "path": file_path,
                        "source": "nextcloud"
                    }]
                )

            print(f"Indexed {file_path}")

        except Exception as e:

            print(
                f"Error indexing {file_path}: {e}"
            )


if __name__ == "__main__":

    index_documents()
