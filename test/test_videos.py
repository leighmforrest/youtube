from youtube.videos import get_video_data_from_api


def test_get_video_data_from_api(mock_response_get_videos):
    results = get_video_data_from_api("TestPlaylistID")
    n_videos = len(results)
    print(n_videos)