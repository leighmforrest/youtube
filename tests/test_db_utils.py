import pytest
import pandas as pd

from youtube.db.utils import (
    get_recent_channel_stats,
    find_videos_with_no_or_old_stats,
    create_time_series_dataframe,
)


class TestGetRecentChannelStats:
    def test_get_recent_channel_stats_success(
        self, test_channel, test_session, test_channel_stats
    ):
        results = get_recent_channel_stats(test_session, test_channel)
        assert results == test_channel_stats

    def test_get_recent_channel_stats_none(self, test_channel, test_session):
        results = get_recent_channel_stats(test_session, test_channel)
        assert results is None

    def test_get_recent_channel_stats_none(
        self, test_channel, test_session, test_channel_stats_old
    ):
        results = get_recent_channel_stats(test_session, test_channel)
        assert results is None


class TestFindVideosWithNoOrOldStats:
    def test_find_videos_with_no_or_old_stats_no_olds(
        self, test_five_videos_stats_current, test_channel, test_session
    ):
        result = find_videos_with_no_or_old_stats(test_session, test_channel)
        assert len(result) == 0

    def test_find_videos_with_no_or_old_stats_seven_old_stats(
        self, test_seven_videos_with_old_stats, test_channel, test_session
    ):
        result = find_videos_with_no_or_old_stats(test_session, test_channel)

        youtube_ids = [
            video.youtube_video_id for video in test_seven_videos_with_old_stats
        ]
        assert len(result) == 7
        for youtube_id in youtube_ids:
            assert youtube_id in result

    def test_find_videos_with_no_or_old_stats_no_five_videos_with_no_stats(
        self, test_session, test_five_videos, test_channel
    ):
        result = find_videos_with_no_or_old_stats(test_session, test_channel)
        youtube_ids = [video.youtube_video_id for video in test_five_videos]
        assert len(result) == 5

        for youtube_id in youtube_ids:
            assert youtube_id in result

    def test_find_videos_with_no_or_old_stats_no_and_old_video_stats(
        self,
        test_session,
        test_five_videos,
        test_seven_videos_with_old_stats,
        test_channel,
    ):
        result = find_videos_with_no_or_old_stats(test_session, test_channel)

        # combine the old stat videos and no stat videos
        test_videos = test_five_videos + test_seven_videos_with_old_stats
        youtube_ids = [video.youtube_video_id for video in test_videos]
        assert len(result) == 12

        for youtube_id in youtube_ids:
            assert youtube_id in result


class TestCreateTimeSeriesDataframe:
    def test_generate_dataframe(
        self, test_session, test_five_videos_stats_current, test_channel
    ):
        results = create_time_series_dataframe(test_session, test_channel)
        assert isinstance(results, pd.DataFrame)
        columns = results.columns
        assert len(columns) == 6
        assert len(results) == 5

        for column in columns:
            assert (
                results[column].notnull().all()
            ), f"Column {column} contains null values"

    def test_dataframe_index(
        self, test_session, test_five_videos_stats_current, test_channel
    ):
        results = create_time_series_dataframe(test_session, test_channel)
        indices = results.index.names
        assert "published_at" in indices

    def test_generate_dataframe_with_old_stats(
        self,
        test_session,
        test_five_videos_stats_current,
        test_seven_videos_with_old_stats,
        test_channel,
    ):
        results = create_time_series_dataframe(test_session, test_channel)
        columns = results.columns
        assert len(columns) == 6
        assert len(results) == 5

        for column in columns:
            assert (
                results[column].notnull().all()
            ), f"Column {column} contains null values"
