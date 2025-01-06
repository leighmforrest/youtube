from datetime import datetime
from youtube.videos import (
    get_video_ids_from_api,
    get_video_data_from_api,
    get_video_stats_from_api,
)


class TestVideos:
    def test_get_video_ids_from_api(self, mock_youtube_playlist_items_api_request):
        results = get_video_ids_from_api("FakePlalistId")
        assert len(results) == 150

    def test_get_video_ids_from_api(self, mock_youtube_playlist_items_api_request):
        results = get_video_ids_from_api("FakePlalistId")

        for result in results:
            assert isinstance(result, str)

    def test_get_video_data_from_api(
        self, mock_youtube_video_api_request, mock_youtube_video_ids
    ):
        results = get_video_data_from_api(mock_youtube_video_ids)
        assert len(results) == 150

    def test_get_video_data_from_api_all_keys(
        self, mock_youtube_video_api_request, mock_youtube_video_ids
    ):
        results = get_video_data_from_api(mock_youtube_video_ids)
        for result in results:
            data = result[0]
            assert isinstance(data["youtube_video_id"], str)
            assert isinstance(data["published_at"], datetime)
            assert isinstance(data["title"], str)
            assert isinstance(data["description"], str)
            assert isinstance(data["thumbnail_url"], str)

    def test_get_video_data_stats_from_api_all_keys(
        self, mock_youtube_video_statistics_api_request, mock_youtube_video_ids
    ):
        results = get_video_stats_from_api(mock_youtube_video_ids)
        for result in results:
            assert isinstance(result["youtube_video_id"], str)
            assert isinstance(result["view_count"], int)
            assert isinstance(result["like_count"], int)
            assert isinstance(result["favorite_count"], int)
            assert isinstance(result["comment_count"], int)

    def test_get_video_stats_from_api(
        self, mock_youtube_video_ids, mock_youtube_video_statistics_api_request
    ):
        results = get_video_stats_from_api(mock_youtube_video_ids)
        assert len(results) == 150
