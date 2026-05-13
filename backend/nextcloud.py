import os
import requests

BASE_URL = os.getenv("NEXTCLOUD_URL", "https://10.0.5.25")
USER = os.getenv("NEXTCLOUD_USER")
PASS = os.getenv("NEXTCLOUD_PASS")


def list_files():
    # Beispiel: echte WebDAV Struktur
    return [
        "/remote.php/dav/files/ai_user/Nextcloud Manual.pdf",
        "/remote.php/dav/files/ai_user/Reasons to use Nextcloud.pdf",
        "/remote.php/dav/files/ai_user/Readme.md"
    ]


def download_file(path):
    url = f"{BASE_URL}{path}"

    r = requests.get(
        url,
        auth=(USER, PASS),
        verify=False,
        timeout=60
    )

    return r.content
