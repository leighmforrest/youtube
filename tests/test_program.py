import pytest

import matplotlib.pyplot as plt

from tests.data import (
    mock_request_channel_data,
    mock_request_channel_stats,
    mock_video_ids,
    mock_request_video_data,
    mock_request_video_stats,
)
from youtube.program import (
    get_channel_data,
    get_video_ids_not_in_database,
    get_video_data,
    get_video_stats,
    create_graph_from_dataframe,
    save_to_csv,
    display_stats_from_dataframe,
    display_channel_stats,
)
from youtube.utils import remove_at_symbol, snake_to_capitals
from youtube.db.utils import get_recent_channel_stats, find_videos_with_no_or_old_stats
from youtube.db.models import Channel, ChannelStats


class TestGetProgramData:
    def test_get_channel_data_new_channel(self, test_handle, test_session, mocker):
        mock_channel_data = mocker.patch("youtube.program.request_channel_data")
        mock_channel_stats = mocker.patch("youtube.program.request_channel_stats")

        mock_channel_data.side_effect = lambda handle: mock_request_channel_data(handle)
        mock_channel_stats.side_effect = lambda handle: mock_request_channel_stats(
            handle
        )

        result = get_channel_data(test_handle, test_session)
        assert isinstance(result, Channel)
        assert isinstance(result.channel_stats[0], ChannelStats)

    def test_get_channel_data_old_channel(
        self, test_handle, test_session, test_channel_stats, test_channel, mocker
    ):
        result = get_channel_data(test_handle, test_session)

        current_channel_stats = get_recent_channel_stats(test_session, test_channel)
        assert isinstance(result, Channel)
        assert current_channel_stats == test_channel_stats

    def test_get_channel_data_old_channel_old_stats(
        self, test_handle, test_session, test_channel, test_channel_stats_old, mocker
    ):
        result = get_channel_data(test_handle, test_session)

        # retrieve the current channel stats
        current_channel_stats = get_recent_channel_stats(test_session, test_channel)
        assert isinstance(result, Channel)
        assert current_channel_stats != test_channel_stats_old


class TestGetVideoIdsNotInDatabase:
    def test_get_video_ids_not_in_database_all_saved(
        self, test_channel, test_session, test_five_videos
    ):
        video_ids = [video.youtube_video_id for video in test_five_videos]
        result = get_video_ids_not_in_database(video_ids, test_session)
        assert len(result) == 0

    def test_get_video_ids_not_in_database_none_saved(
        self,
        test_channel,
        test_session,
    ):
        test_video_ids = mock_video_ids(10)
        result = get_video_ids_not_in_database(test_video_ids, test_session)
        assert len(result) == 10

    def test_get_video_ids_not_in_database_both_saved_and_unsaved(
        self,
        test_channel,
        test_session,
        test_five_videos,
        test_seven_videos_with_old_stats,
    ):
        nonexistant_videos = mock_request_channel_stats(10)
        result = get_video_ids_not_in_database(nonexistant_videos, test_session)
        assert len(result) == len(nonexistant_videos)

    def test_get_video_data_all_already_saved(
        self, test_session, test_channel, test_five_videos_stats_current, capsys, mocker
    ):
        test_video_ids = [
            stats.video.youtube_video_id for stats in test_five_videos_stats_current
        ]
        mock_video_ids = mocker.patch("youtube.program.get_video_ids_from_api")
        mocker.return_value = mock_video_ids

        get_video_data(test_channel, test_session)
        captured = capsys.readouterr()

        assert "All videos are already saved in the database." in captured.out

    def test_get_video_data_none_saved(
        self, test_session, test_channel, capsys, mocker
    ):
        test_video_ids = mock_video_ids(5)
        mock_nonexistant_video_ids = mocker.patch(
            "youtube.program.get_video_ids_from_api"
        )
        mock_video_data = mocker.patch("youtube.program.get_video_data_from_api")

        mock_nonexistant_video_ids.return_value = test_video_ids
        mock_video_data.side_effect = mock_request_video_data

        results = get_video_data(test_channel, test_session)
        captured = capsys.readouterr()

        assert f"Found {len(test_video_ids)} new videos to save." in captured.out
        print(f"Saved {len(test_video_ids)} new videos.")

    def test_get_video_stats_all_olds(
        self,
        test_session,
        test_channel,
        test_seven_videos_with_old_stats,
        mocker,
        capsys,
    ):
        mock_video_stats = mocker.patch("youtube.program.get_video_stats_from_api")
        mock_video_stats.side_effect = mock_request_video_stats

        get_video_stats(test_channel, test_session)
        assert not find_videos_with_no_or_old_stats(test_session, test_channel)

    def test_get_video_stats_all_current(
        self,
        test_session,
        test_channel,
        test_five_videos_stats_current,
        mocker,
        capsys,
    ):
        mock_video_stats = mocker.patch("youtube.program.get_video_stats_from_api")
        mock_video_stats.side_effect = mock_request_video_stats

        get_video_stats(test_channel, test_session)
        captured = capsys.readouterr()

        assert "All videos have up-to-date stats." in captured.out
        assert not find_videos_with_no_or_old_stats(test_session, test_channel)


class TestCreateGraphFromFataframe:
    @pytest.mark.parametrize("metric", ["view_count", "like_count", "comment_count"])
    def test_graph_created(self, metric, test_dataframe, mocker):
        mock_show = mocker.patch("youtube.program.plt.show")
        mock_figure = mocker.patch(
            "youtube.program.plt.figure", return_value=plt.figure()
        )

        create_graph_from_dataframe(test_dataframe, metric)
        mock_show.assert_called_once()
        mock_figure.assert_called_once()


class TestSaveToCSV:
    def test_save_to_csv(self, test_dataframe, tmpdir, test_handle):
        filename = f"{remove_at_symbol(test_handle)}.csv"
        file_path = tmpdir / filename
        save_to_csv(test_dataframe, file_path)
        assert file_path.exists()


class TestDisplayStatsFromDataframe:
    metric_names = ["view_count", "like_count", "comment_count"]

    def test_display_stats_from_dataframe_header(self, test_dataframe, capsys):
        display_stats_from_dataframe(test_dataframe)
        captured = capsys.readouterr()

        assert (
            f"{'Metric':<15}|{'Mean':<15}|{'Median':<15}|{'Std Dev':<15}"
            in captured.out
        )

    @pytest.mark.parametrize("metric", metric_names)
    def test_display_stats_from_dataframe(self, metric, test_dataframe, capsys):
        display_stats_from_dataframe(test_dataframe)
        captured = capsys.readouterr()

        assert snake_to_capitals(metric) in captured.out


class TestDisplayChannelStats:
    def test_display_channel_stats(
        self, test_session, test_channel, test_channel_stats, capsys
    ):
        test_stats = get_recent_channel_stats(test_session, test_channel)
        display_channel_stats(test_session, test_channel)
        captured = capsys.readouterr()

        assert f"Stats for {test_channel.handle}" in captured.out
        assert f"{test_stats.video_count}" in captured.out
        assert f"{test_stats.view_count}" in captured.out
        assert f"{test_stats.subscriber_count}" in captured.out
