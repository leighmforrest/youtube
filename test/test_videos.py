from youtube.videos import extract_video_ids, get_video_statistics_from_api


def test_get_video_data_from_api(testing_get_video_data_from_api):
    n_videos = len(testing_get_video_data_from_api)
    assert n_videos == 150

    for result in testing_get_video_data_from_api:
        assert "video_id" in result
        assert "thumbnail_url" in result
        assert "title" in result


def test_get_video_statistics_from_api(
    testing_get_video_data_from_api, mock_requests_get_video_statistics
):
    video_ids = extract_video_ids(testing_get_video_data_from_api)
    stats = get_video_statistics_from_api(video_ids)

    for stat in stats:
        assert "youtube_video_id" in stat
        assert "view_count" in stat
        assert "like_count" in stat
        assert "comment_count" in stat
