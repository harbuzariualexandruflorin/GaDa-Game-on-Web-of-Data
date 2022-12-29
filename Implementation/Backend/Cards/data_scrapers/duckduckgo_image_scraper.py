import json
import re
import time

import requests


def get_first_filtered_url(data, filters):
    images = data.get("results", [])
    if len(images) == 0:
        return None

    for img in images:
        if img.get("image", None) is None:
            continue

        is_good = True
        for f in filters:
            if f not in img["image"]:
                is_good = False
                break
        if is_good:
            return img["image"]
    return None


def search_image(keyword, filters):
    url = 'https://duckduckgo.com/'
    params = {'q': keyword}
    res = requests.post(url, data=params)
    searchObj = re.search(r'vqd=([\d-]+)&', res.text, re.M | re.I)
    if not searchObj:
        print("DUCKDUCKGO IMAGE SCRAPER ERROR: Token Parsing Failed!")
        return None

    headers = {'referer': 'https://duckduckgo.com/'}
    params = (
        ('l', 'us-en'),
        ('o', 'json'),
        ('q', keyword),
        ('vqd', searchObj.group(1)),
        ('f', ',,,'),
        ('p', '1'),
        ('v7exp', 'a'),
    )
    requestUrl = url + "i.js"

    while True:
        try:
            res = requests.get(requestUrl, headers=headers, params=params)
            data = json.loads(res.text)

            filtered_url = get_first_filtered_url(data, filters)
            if filtered_url is not None:
                return filtered_url

            if "next" not in data:
                return None
            requestUrl = url + data["next"]
        except Exception:
            print("DUCKDUCKGO IMAGE SCRAPER ERROR: Hitting Url Failure. Sleep and Retry: ", requestUrl)
            time.sleep(10)
            continue
