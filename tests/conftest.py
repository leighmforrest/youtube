import pytest
from tests.mocks import MockResponse
from tests.data import (
    mock_channels_list_api_data,
    mock_channels_list_api_stats,
    mock_request_playlist_items_api_paginated_dictionary,
    mock_video_ids,
    mock_request_video_api_data,
    mock_request_video_api_statistics,
)


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
def mock_channel_list_api_data_request(mocker):
    test_response_data = mock_channels_list_api_data(test_handle)
    mock_get_youtube_request = mocker.patch(
        "youtube.channels.get_youtube_request",
        return_value=test_response_data,
    )

    return mock_get_youtube_request


@pytest.fixture
def mock_channel_list_api_stats_request(mocker):
    test_response_data = mock_channels_list_api_stats(test_handle)
    mock_get_youtube_request = mocker.patch(
        "youtube.channels.get_youtube_request",
        return_value=test_response_data,
    )

    return mock_get_youtube_request


@pytest.fixture
def mock_youtube_playlist_items_pages():
    return mock_request_playlist_items_api_paginated_dictionary()


@pytest.fixture
def mock_youtube_playlist_items_api_request(mock_youtube_playlist_items_pages, mocker):
    def mock_request(endpoint, params):
        page_token = params.get("pageToken", None)
        if page_token in mock_youtube_playlist_items_pages:
            return mock_youtube_playlist_items_pages[page_token]
        else:
            raise ValueError(f"Invalid pageToken: {page_token}")

    mock = mocker.patch("youtube.videos.get_youtube_request", side_effect=mock_request)

    return mock


@pytest.fixture
def mock_youtube_video_ids():
    return mock_video_ids()


@pytest.fixture
def mock_youtube_video_api_request(mock_youtube_video_ids, mocker):
    def mock_request(endpoint, params):
        ids = params.get("id")
        # The id parameter is a comma-separated list of video ids, so split them
        video_ids = ids.split(",") if ids else []
        return mock_request_video_api_data(video_ids)

    mock = mocker.patch("youtube.videos.get_youtube_request", side_effect=mock_request)

    return mock


@pytest.fixture
def mock_youtube_video_statistics_api_request(mock_youtube_video_ids, mocker):
    def mock_request(endpoint, params):
        ids = params.get("id")
        # The id parameter is a comma-separated list of video ids, so split them
        video_ids = ids.split(",") if ids else []
        return mock_request_video_api_statistics(video_ids)

    mock = mocker.patch("youtube.videos.get_youtube_request", side_effect=mock_request)

    return mock
