import requests
from datetime import datetime
from pprint import pprint
from settings import YOUTUBE_KEY, BASE_URL


def extract_video_ids(videos):
    return [video["video_id"] for video in videos]


def get_video_data(playlist_id="UUT3EznhW_CNFcfOlyDNTLLw", max_results=50):
    params = {
        "key": YOUTUBE_KEY,
        "part": "snippet",
        "playlistId": playlist_id,
        "maxResults": max_results,
    }

    videos = []
    url = f"{BASE_URL}/playlistItems"

    while True:
        response = requests.get(url, params)
        if response.status_code != 200:
            print(f"Error fetching playlist data: {response.status_code}")
            break

        data = response.json()
        playlist_data = data.get("items", [])
        for datum in playlist_data:
            video_data = datum.get("snippet", {})
            resource_id = video_data.get("resourceId", {})
            if resource_id.get("kind") == "youtube#video":
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

                videos.append(cleaned_data)

        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break
        params["pageToken"] = next_page_token

    return videos


def get_video_statistics(video_ids, max_batch_size=50):
    stats = []
    url = f"{BASE_URL}/videos"

    for i in range(0, len(video_ids), max_batch_size):
        batch_ids = video_ids[i : i + max_batch_size]
        params = {"key": YOUTUBE_KEY, "part": "statistics", "id": ",".join(batch_ids)}

        response = requests.get(url, params)
        if response.status_code != 200:
            print(f"Error fetching video statistics: {response.status_code}")
            continue

        data = response.json()
        for item in data.get("items", []):
            video_id = item["id"]
            statistics = item.get("statistics", {})
            stats.append(
                {
                    "video_id": video_id,
                    "view_count": int(statistics.get("viewCount", 0)),
                    "like_count": int(statistics.get("likeCount", 0)),
                    "comment_count": int(statistics.get("commentCount", 0)),
                }
            )

    return stats