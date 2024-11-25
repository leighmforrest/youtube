from youtube.videos import extract_video_ids, get_video_statistics_from_api


def test_get_video_from_api(videos_from_api):
    assert len(videos_from_api) == 150


def test_extract_video_ids(videos_from_api):
    video_ids = extract_video_ids(videos_from_api)
    assert isinstance(video_ids, list)
    assert len(video_ids) == 150


def test_get_video_statistics_normal(mock_requests_get_video_statistics):
    video_ids = [f"YouTUbeID_{i}" for i in range(20)]
    stats = get_video_statistics_from_api(video_ids, max_batch_size=5)

    assert len(stats) == 20
    
    for stat in stats:
        assert "video_id" in stat
        assert "view_count" in stat
        assert "like_count" in stat
        assert "comment_count" in stat


def test_get_video_statistics_error(mock_requests_get_video_statistics_error):
    video_ids = [f"YouTUbeID_{i}" for i in range(20)]
    stats = get_video_statistics_from_api(video_ids, max_batch_size=5)
    
    assert stats == []


def test_get_video_statistics_empty_ids(mock_requests_get_video_statistics):
    stats = get_video_statistics_from_api([], max_batch_size=5)
    assert stats == []


def test_get_video_statistics_partial_batch(mock_requests_get_video_statistics):
    video_ids = [f"YouTUbeID_{i}" for i in range(7)]
    stats = get_video_statistics_from_api(video_ids, max_batch_size=5)
    assert len(stats) == 7
