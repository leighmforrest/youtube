import requests

from youtube.request import get_youtube_request


def extract_channel_data(handle, data):
    """Filters the response and prepares all data needed for function return."""
    # extract the parts
    snippet = data["snippet"]
    content_details = data["contentDetails"]

    # this channel is youtube's id
    youtube_channel_id = data["id"]

    # necessary data parts
    title = snippet["title"]
    description = snippet["description"]
    thumbnail_url = snippet["thumbnails"]["default"]["url"]
    uploads_playlist = content_details["relatedPlaylists"]["uploads"]

    return {
        "handle": handle,
        "youtube_channel_id": youtube_channel_id,
        "title": title,
        "description": description,
        "thumbnail_url": thumbnail_url,
        "uploads_playlist": uploads_playlist,
    }


def extract_channel_stats(handle, data):
    stats = data["statistics"]

    view_count = stats["viewCount"]
    subscriber_count = stats["subscriberCount"]
    video_count = stats["videoCount"]

    return {
        "handle": handle,
        "view_count": view_count,
        "subscriber_count": subscriber_count,
        "video_count": video_count,
    }


def request_channel_data(handle: str):
    try:
        params = {"forHandle": handle, "part": "snippet,contentDetails"}
        response = get_youtube_request(params=params)
        channel = response.get("items")[0]

        data = extract_channel_data(handle, channel)

        return data
    except requests.exceptions.HTTPError as e:
        print(f"An error occurred while requesting channel data for handle: {handle}")
        print(f"Error details: {e}")
        return None


def request_channel_stats(handle: str):
    try:
        params = {"forHandle": handle, "part": "statistics"}
        response = get_youtube_request(params=params)
        channel = response.get("items")[0]

        data = extract_channel_stats(handle, channel)

        return data
    except requests.exceptions.HTTPError as e:
        print(f"An error occurred while requesting channel data for handle: {handle}")
        print(f"Error details: {e}")
        return None
