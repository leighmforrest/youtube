from datetime import datetime
from youtube.channels import request_channel_data
from videos import get_video_ids_from_api
from videos import get_video_data_from_api, get_video_stats_from_api


if __name__ == "__main__":
    handle = "@RickBeato"
    channel_data = request_channel_data(handle)
    playlist_id = channel_data["uploads_playlist"]
    video_ids = get_video_ids_from_api(playlist_id)
    videos = get_video_stats_from_api(video_ids)
    print(videos)
