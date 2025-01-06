from youtube.request import get_youtube_request


def get_video_ids_from_api(playlist_id: str):
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
