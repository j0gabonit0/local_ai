import time
from core.nextcloud import list_files, download_file, file_hash
from core.index import upsert_doc

seen = {}

def run_watcher():

    while True:

        files = list_files("/")

        for f in files:

            content = download_file(f["path"])
            h = file_hash(content)

            if f["path"] not in seen or seen[f["path"]] != h:

                print("INDEX:", f["path"])

                upsert_doc(
                    text=content.decode(errors="ignore"),
                    metadata={
                        "path": f["path"],
                        "groups": f["groups"]
                    }
                )

                seen[f["path"]] = h

        time.sleep(20)
