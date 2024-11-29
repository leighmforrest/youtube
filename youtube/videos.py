import logging
from datetime import datetime
from pprint import pprint

import requests

from youtube.settings import BASE_URL, YOUTUBE_KEY

logging.basicConfig(level=logging.INFO)


def extract_video_ids(videos: list) -> list:
    """Extract YouTube video IDs from a list of video data dictionaries."""
    return [video["video_id"] for video in videos]


def extract_video_api_data(resource_id: dict, video_data: dict) -> dict:
    """Clean video data from the YouTube API snippet."""
    published_at_iso_string = video_data.get("publishedAt")
    try:
        published_at = datetime.fromisoformat(
            published_at_iso_string.replace("Z", "+00:00")
        )
    except (TypeError, ValueError):
        logging.warning(f"Invalid publishedAt: {published_at_iso_string}")
        published_at = None

    return {
        "video_id": resource_id.get("videoId"),
        "thumbnail_url": video_data.get("thumbnails", {})
        .get("standard", {})
        .get("url"),
        "title": video_data.get("title"),
        "published_at": published_at,
    }


def get_video_data_from_api(playlist_id: str) -> list:
    """Fetch video data from the YouTube API given a playlist ID."""
    url = f"{BASE_URL}/playlistItems"
    params = {
        "key": YOUTUBE_KEY,
        "part": "snippet",
        "playlistId": playlist_id,
        "maxResults": 50,
    }
    videos = []

    while True:
        response = requests.get(url, params)
        if response.status_code != 200:
            logging.error(f"Error fetching playlist data: {response.status_code}")
            break

        data = response.json()
        playlist_items = data.get("items", [])

        for item in playlist_items:
            snippet = item.get("snippet")
            resource_id = snippet.get("resourceId", {})
            if resource_id.get("kind") == "youtube#video":
                cleaned_data = extract_video_api_data(resource_id, snippet)
                videos.append(cleaned_data)

        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break
        params["pageToken"] = next_page_token

    return videos


def get_video_statistics_from_api(video_ids: list, max_batch_size: int = 50) -> list:
    """Fetch statistics for a list of video IDs from the YouTube API."""
    url = f"{BASE_URL}/videos"
    stats = []

    for i in range(0, len(video_ids), max_batch_size):
        batch_ids = video_ids[i : i + max_batch_size]
        params = {
            "key": YOUTUBE_KEY,
            "part": "statistics",
            "id": ",".join(batch_ids),
        }

        response = requests.get(url, params)
        if response.status_code != 200:
            print(f"Error fetching video statistics: {response.status_code}")
            continue

        data = response.json()
        items = data.get("items")

        for item in items:
            youtube_video_id = item.get("id")
            statistics = item.get("statistics")
            video_stats = {
                "youtube_video_id": youtube_video_id,
                "comment_count": statistics.get("commentCount", 0),
                "like_count": statistics.get("likeCount", 0),
                "view_count": statistics.get("viewCount", 0),
            }
            stats.append(video_stats)

    return stats
