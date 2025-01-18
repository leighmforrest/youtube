from tests.data import mock_request_channel_data, mock_request_channel_stats
from youtube.program import get_channel_data
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
        self, test_handle, test_session, test_channel_stats, mocker
    ):
        result = get_channel_data(test_handle, test_session)
        assert isinstance(result, Channel)
        assert isinstance(result.channel_stats[0], ChannelStats)
        assert result.channel_stats[0] == test_channel_stats
