import requests

from youtube.settings import YOUTUBE_API_KEY, BASE_URL


BASE_PARAMS = {"key": YOUTUBE_API_KEY}


def get_youtube_request(endpoint="channels", params=None, headers=None):
    if params is None:
        params = {}

    params = {**params, **BASE_PARAMS}
    url = f"{BASE_URL}{endpoint}"

    response = requests.get(url, params)
    response.raise_for_status()
    return response.json()
