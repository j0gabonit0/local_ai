import requests
import os

URL = os.getenv("NEXTCLOUD_URL", "https://10.0.5.25")
USER = os.getenv("NEXTCLOUD_USER")
PASS = os.getenv("NEXTCLOUD_PASSWORD")

VERIFY_SSL = False


# ----------------------------
# LIST FILES VIA WEBDAV
# ----------------------------
def list_files(path="/"):

    url = f"{URL}/remote.php/dav/files/{USER}/"

    r = requests.request(
        "PROPFIND",
        url,
        auth=(USER, PASS),
        headers={"Depth": "1"},
        verify=VERIFY_SSL
    )

    if r.status_code not in [200, 207]:
        print("WebDAV ERROR:", r.status_code)
        return []

    import xml.etree.ElementTree as ET

    root = ET.fromstring(r.text)

    files = []

    for response in root.findall(".//{DAV:}response"):

        href = response.find("{DAV:}href")

        if href is None or href.text is None:
            continue

        path = href.text

        if path.endswith("/"):
            continue

        print("FOUND:", path)
        files.append(path)

    return files


# ----------------------------
# DOWNLOAD FILE CONTENT
# ----------------------------
def download_file(file_path):

    url = f"{URL}{file_path}"

    r = requests.get(
        url,
        auth=(USER, PASS),
        verify=VERIFY_SSL
    )

    print("DOWNLOAD:", url, r.status_code)

    if r.status_code != 200:
        return ""

    content_type = r.headers.get("Content-Type", "")

    # nur Text für RAG
    if "text" in content_type or "markdown" in content_type:
        return r.text

    if "pdf" in content_type:
        return f"[PDF FILE: {file_path}]"

    return ""
