import requests

from youtube.settings import BASE_URL, YOUTUBE_API_KEY

BASE_PARAMS = {"key": YOUTUBE_API_KEY}


def get_youtube_request(
    endpoint: str = "channels", params: dict = None, headers: dict = None
) -> dict:
    """Make a request to a YouTube API endpoint. Default endpoint is channels."""
    if params is None:
        params = {}

    params = {**params, **BASE_PARAMS}
    url = f"{BASE_URL}{endpoint}"

    response = requests.get(url, params)
    response.raise_for_status()
    return response.json()
