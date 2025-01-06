from channel import request_channel_data, request_channel_stats
from videos import get_video_ids_from_api
from tests.data import mock_request_playlist_items_api_paginated_dictionary


if __name__ == "__main__":
    handle = "@RickBeato"
    channel_data = request_channel_data("@RickBeato")
    channel_stats = request_channel_stats(handle)
    playlist_id = channel_data["uploads_playlist"]
    print(channel_data)
    print(channel_stats)
    print(f"The YouTube Uploads Playlist id is {playlist_id}")
    video_ids = get_video_ids_from_api(playlist_id)
    print(video_ids)
    print(len(video_ids))
