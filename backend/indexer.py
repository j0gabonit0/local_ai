from nextcloud import list_files, download_file
from vectorstore import add_doc


def index_nextcloud():

    files = list_files()

    print("FILES:", files)

    count = 0

    for f in files:

        try:
            content = download_file(f)

            if not content:
                continue

            add_doc(content, {"source": f})

            count += 1

        except Exception as e:
            print("INDEX ERROR:", f, e)
            continue

    return {
        "files": len(files),
        "count": count
    }
