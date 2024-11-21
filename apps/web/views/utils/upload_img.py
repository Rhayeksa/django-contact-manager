import json

import requests


def upload_img(
    img,
    url: str,
    key: str
):
    result = requests.post(
        url=url,
        data={"key": key},
        files={"image": img}
    )
    return json.dumps(result.json())
