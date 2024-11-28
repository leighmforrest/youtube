import pytest
import requests

from test.helpers import generate_paginated_responses
from test.mocks import MockResponse
from test.factories.channels import YouTubeChannelListResponseFactory, YouTubeChannelStatisticsResponseFactory


@pytest.fixture
def test_handle():
    return "@OurTubeChannel"


@pytest.fixture
def channel_data():
    return YouTubeChannelListResponseFactory()


@pytest.fixture
def channel_statistics():
    return YouTubeChannelStatisticsResponseFactory()


@pytest.fixture
def mock_response_generic(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse(json_data={"message": "response"})
    
    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_response_channel_data(monkeypatch, channel_data):
    def mock_get(*args, **kwargs):
        return MockResponse(json_data=channel_data)
    
    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_response_channel_statistics(monkeypatch, channel_statistics):
    def mock_get(*args, **kwargs):
        return MockResponse(json_data=channel_statistics)
    
    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_paginated_video_responses():
    return generate_paginated_responses()


@pytest.fixture
def mock_response_get_videos(monkeypatch, mock_paginated_video_responses):
    def mock_get(url, params=None,*args, **kwargs):
        next_page_token = params.get("pageToken") if params else None

        response_data = mock_paginated_video_responses.get(next_page_token)
        if response_data:
            return MockResponse(json_data=response_data)
        return MockResponse(status_code=404, text_data="Not Found")
    
    monkeypatch.setattr(requests, "get", mock_get)
