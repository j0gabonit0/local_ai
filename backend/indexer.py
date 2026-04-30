from nextcloud import list_files, download_file
from vectorstore import add_doc


def index_nextcloud():

    files = list_files()

    count = 0

    for f in files:

        content = download_file(f)

        if not content:
            continue

        add_doc(content, {"source": f})
        count += 1

    return {
        "files": len(files),
        "count": count
    }
