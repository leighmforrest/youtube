from tests.data import mock_channels_list_api_data
from requests.exceptions import HTTPError
from youtube.channel import request_channel_data


class TestChannel:
    def test_request_channel_data(self, mock_channel_list_api_request, test_handle):
        test_response = mock_channels_list_api_data(test_handle)
        test_params = {"forHandle": test_handle, "part": "snippet,contentDetails"}

        result = request_channel_data(test_handle)
        mock_channel_list_api_request.assert_called_once_with(params=test_params)

        assert result["handle"] == test_handle
        assert isinstance(result["youtube_channel_id"], str)
        assert isinstance(result["title"], str)

    def test_request_channel_data_error(self, mocker, test_handle):
        mock_get_youtube_request = mocker.patch(
            "youtube.channel.get_youtube_request", side_effect=HTTPError
        )

        result = request_channel_data(test_handle)
        assert result is None
