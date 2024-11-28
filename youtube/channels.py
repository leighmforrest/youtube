import requests
from youtube.utils import ensure_at_symbol
from youtube.settings import BASE_URL, YOUTUBE_KEY


def extract_channel_api_data(channel_item: dict, handle: str):
    """Data from the API that is used in the application."""
    channel_data = channel_item["items"][0]
    snippet = channel_data["snippet"]
    upload_playlist = channel_data["contentDetails"]["relatedPlaylists"]["uploads"]

    # get the needed data from the request
    extracted_data = {
        "handle": handle,
        "youtube_channel_id": channel_data["id"],
        "title": snippet["title"],
        "description": snippet["description"],
        "thumbnail_url": snippet["thumbnails"]["default"]["url"],
        "upload_playlist": upload_playlist
    }

    return extracted_data


def extract_channel_statistics(channel_api_data: dict):
    statistics = channel_api_data["items"][0]["statistics"]

    cleaned_statistics = {
        "subscriber_count": int(statistics["subscriberCount"]),
        "video_count": int(statistics["videoCount"]),
        "view_count": int(statistics["viewCount"]),
    }

    return cleaned_statistics


def get_channel_data_from_api(handle):
    handle = ensure_at_symbol(handle)
    url = f"{BASE_URL}/channels"
    channel_params = {
        "key": YOUTUBE_KEY,
        "part": "snippet,contentDetails",
        "forHandle": handle
    }

    # Fetch channel data
    response = requests.get(url, channel_params)
    channel_data = response.json()
    
    extracted_data = extract_channel_api_data(channel_data, handle)
    return extracted_data


def get_channel_statistics_from_api(handle):
    handle = ensure_at_symbol(handle)
    url = f"{BASE_URL}/channels"
    channel_params = {
        "key": YOUTUBE_KEY,
        "part": "statistics",
        "forHandle": handle
    }

    # Fetch channel data
    response = requests.get(url, channel_params)
    channel_data = response.json()
    
    extracted_data = extract_channel_statistics(channel_data)
    return extracted_data
