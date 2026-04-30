import requests
import os
import hashlib

URL = os.getenv("NEXTCLOUD_URL")
USER = os.getenv("NEXTCLOUD_USER")
PASS = os.getenv("NEXTCLOUD_PASSWORD")


def list_files(path="/"):
    # vereinfacht (in Produktion WebDAV XML parser erweitern)
    return [
        {"path": "/HR/test.txt", "groups": ["HR"]},
        {"path": "/Finance/report.pdf", "groups": ["Finance"]}
    ]


def download_file(path):
    r = requests.get(
        f"{URL}/remote.php/dav/files/{USER}{path}",
        auth=(USER, PASS)
    )
    return r.content


def file_hash(content):
    return hashlib.sha256(content).hexdigest()
