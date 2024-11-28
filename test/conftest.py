import pytest
import requests

from test.mocks import MockResponse
from test.factories import YouTubeChannelListResponseFactory, YouTubeChannelStatisticsResponseFactory


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