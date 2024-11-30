from pprint import pprint

from youtube.channels import get_channel_data_from_api, get_channel_statistics_from_api
from youtube.videos import (
    extract_video_ids,
    get_video_data_from_api,
    get_video_statistics_from_api,
)

if __name__ == "__main__":
    handle = "RickBeato"
    channel_data = get_channel_data_from_api(handle)
    channel_statistics = get_channel_statistics_from_api(handle)
    pprint(channel_data)
    pprint(channel_statistics)
    playlist_id = channel_data["upload_playlist"]
    videos = get_video_data_from_api(playlist_id)
    pprint(videos)
    video_ids = extract_video_ids(videos)
    video_stats = get_video_statistics_from_api(video_ids)

    pprint(video_stats)
