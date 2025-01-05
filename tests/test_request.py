import pytest
import requests
from tests.mocks import MockResponse
from tests.data import mock_channels_list_api_data
from youtube.request import get_youtube_request


class TestRequest:
    def test_get_youtube_request_no_args(
        self, mock_response: pytest.MonkeyPatch, test_handle: str
    ):
        """Test YouTube request with no arguments."""
        mock_response(json_data=mock_channels_list_api_data(test_handle))
        result = get_youtube_request()
        items = result["items"][0]
        assert isinstance(items["id"], str)

    def test_get_youtube_request_with_args(
        self, mock_response: pytest.MonkeyPatch, test_handle: str
    ):
        """Test YouTube request with arguments."""
        mock_response(json_data=mock_channels_list_api_data(test_handle))
        params = {"forHandle": test_handle, "part": "snippet,contentDetails"}
        result = get_youtube_request(endpoint="channels", params=params)
        items = result["items"][0]
        assert isinstance(items["id"], str)

    @pytest.mark.parametrize("error", [400, 401, 403, 404, 500])
    def test_get_youtube_request_error(self, error, mock_response):
        mock_response(json_data={"hello": "world"}, status_code=error)
        with pytest.raises(requests.exceptions.HTTPError, match=f"{error} Error"):
            get_youtube_request()
