from datetime import datetime

from youtube.request import get_youtube_request
from youtube.utils import chunk_list, get_total_seconds


def extract_video_data(data: dict) -> dict:
    """Extract needed video data from api data."""
    video_id = data["id"]
    snippet = data["snippet"]
    thumbnails = snippet["thumbnails"]
    content_details = data["contentDetails"]
    raw_published_at = snippet["publishedAt"]
    raw_duration = content_details["duration"]

    published_at = datetime.strptime(raw_published_at, "%Y-%m-%dT%H:%M:%SZ")
    duration = get_total_seconds(raw_duration)
    return {
        "youtube_video_id": video_id,
        "published_at": published_at,
        "title": snippet["title"],
        "description": snippet["description"],
        "thumbnail_url": thumbnails["default"]["url"],
        "duration": duration,
    }


def extract_video_statistics(data: dict) -> dict:
    """Extract needed statistics from api data."""
    video_id = data["id"]
    statistics = data["statistics"]

    return {
        "youtube_video_id": video_id,
        "view_count": statistics.get("viewCount", 0),
        "like_count": statistics.get("likeCount", 0),
        "favorite_count": statistics.get("favoriteCount", 0),
        "comment_count": statistics.get("commentCount", 0),
    }


def get_video_ids_from_api(playlist_id: str) -> list[str]:
    """Retrieve all of the videos in the uploads playlist."""
    params = {"part": "contentDetails", "playlistId": playlist_id, "maxResults": 50}
    video_ids = []

    while True:
        data = get_youtube_request("playlistItems", params=params)
        next_page_token = data.get("nextPageToken")
        items = data.get("items")

        for item in items:
            content_details = item["contentDetails"]
            video_id = content_details["videoId"]
            video_ids.append(video_id)

        if next_page_token:
            params["pageToken"] = next_page_token
        else:
            break

    return video_ids


def get_video_data_from_api(video_ids: list[str]) -> list[tuple[dict, dict]]:
    """Obtain video data and statistics for each video in the list."""
    videos = []
    print("Getting video data from API")
    video_id_chunks = chunk_list(video_ids)

    for chunk in video_id_chunks:
        ids = ",".join(chunk)
        params = {"id": ids, "part": "snippet,contentDetails,statistics"}
        video_list = get_youtube_request("videos", params)
        items = video_list["items"]

        for video in items:
            data = extract_video_data(video)
            stats = extract_video_statistics(video)
            videos.append((data, stats))

    return videos


def get_video_stats_from_api(video_ids: list[str]) -> list[dict]:
    """Obtain video stats and statistics for each video in the list."""
    videos = []
    print("Getting video stats from API")
    video_id_chunks = chunk_list(video_ids)

    for chunk in video_id_chunks:
        ids = ",".join(chunk)
        params = {"id": ids, "part": "statistics"}
        video_list = get_youtube_request("videos", params)
        items = video_list["items"]

        for video in items:
            stats = extract_video_statistics(video)
            videos.append(stats)

    return videos
