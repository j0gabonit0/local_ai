import requests
import os

URL = os.getenv("NEXTCLOUD_URL")


def get_groups(user, password):

    r = requests.get(
        f"{URL}/ocs/v1.php/cloud/users/{user}",
        auth=(user, password),
        headers={"OCS-APIRequest": "true"}
    )

    return r.json()["ocs"]["data"]["groups"]
