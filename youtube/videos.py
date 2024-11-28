import requests
from pprint import pprint
from datetime import datetime
from youtube.settings import YOUTUBE_KEY, BASE_URL


def extract_video_api_data(resource_id: str, video_data: dict):
    published_at_iso_string = video_data.get("publishedAt")
    published_at = datetime.fromisoformat(
        published_at_iso_string.replace("Z", "+00:00")
    )

    cleaned_data = {
        "video_id": resource_id.get("videoId"),
        "thumbnail_url": video_data.get("thumbnails", {})
        .get("standard", {})
        .get("url"),
        "title": video_data.get("title"),
        "published_at": published_at,
    }
    pprint(cleaned_data)
    return cleaned_data


def get_video_data_from_api(playlist_id: str):
    """Get video data from the YouTube API v3, given a playlist ID."""
    params = {
        "key": YOUTUBE_KEY,
        "part": "snippet",
        "playlistId": playlist_id,
        "maxResults": 50,
    }
    url = f"{BASE_URL}/playlistItems"
    videos = []

    while True:
        response = requests.get(url, params)
        if response.status_code != 200:
            print(f"Error fetching playlist data: {response.status_code}")
            break

        data = response.json()
        playlist_data = data.get("items", [])

        pprint(playlist_data)

        for datum in playlist_data:
            snippet = datum.get("snippet")
            resource_id = snippet.get("resourceId", {})
            
            if resource_id.get("kind") == "youtube#video":
                print(snippet["title"], "being added")
                cleaned_data = extract_video_api_data(resource_id, snippet)
                videos.append(cleaned_data)
                pprint(cleaned_data)

        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break
        params["pageToken"] = next_page_token

    return videos