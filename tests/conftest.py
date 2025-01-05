import pytest
from tests.mocks import MockResponse
from tests.data import mock_channels_list_api_data


@pytest.fixture
def test_handle():
    return "@YourTubeChannel"


@pytest.fixture
def mock_response(monkeypatch):
    def _mock_response(json_data, status_code=200):
        def mock_requests_get(*args, **kwargs):
            return MockResponse(json_data=json_data, status_code=status_code)

        monkeypatch.setattr("requests.get", mock_requests_get)

    return _mock_response


@pytest.fixture
def mock_channel_list_api_request(mocker):
    test_response_data = mock_channels_list_api_data(test_handle)
    mock_get_youtube_request = mocker.patch(
        "youtube.channel.get_youtube_request",
        return_value=test_response_data,
    )

    return mock_get_youtube_request
