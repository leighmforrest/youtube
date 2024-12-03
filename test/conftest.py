from test.factories.channels import (
    ChannelFactory,
    VideoFactory,
    YouTubeChannelListResponseFactory,
    YouTubeChannelStatisticsResponseFactory,
)
from test.factories.videos import (
    YouTubeVideoStatisticsItemFactory,
    YouTubeVideoStatisticsResponseFactory,
)
from test.helpers import generate_paginated_responses
from test.mocks import MockResponse

import pytest
import requests
from sqlalchemy.orm import Session

from youtube.db import init_db
from youtube.db.models import Channel
from youtube.videos import get_video_data_from_api


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
    def mock_get(url, params=None, *args, **kwargs):
        next_page_token = params.get("pageToken") if params else None

        response_data = mock_paginated_video_responses.get(next_page_token)
        if response_data:
            return MockResponse(json_data=response_data)
        return MockResponse(status_code=404, text_data="Not Found")

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_requests_get_video_statistics(monkeypatch):

    def mock_get(url, params=None, **kwargs):
        # Simulate response for each batch of video IDs
        video_ids = params.get("id", "").split(",")
        items = [YouTubeVideoStatisticsItemFactory(id=video) for video in video_ids]
        # Generate the response
        response_data = YouTubeVideoStatisticsResponseFactory(items=items)
        return MockResponse(json_data=response_data)

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def testing_get_video_data_from_api(mock_response_get_videos):
    return get_video_data_from_api("TestPlaylistID")


@pytest.fixture(scope="function")
def test_session():
    _, session = init_db("sqlite:///:memory:")

    yield session

    session.rollback()
    session.close()


@pytest.fixture(scope="function")
def test_channel(test_session: Session):
    ChannelFactory._meta.sqlalchemy_session = test_session
    VideoFactory._meta.sqlalchemy_session = test_session
    channel = ChannelFactory(videos=6)
    test_session.add(channel)
    test_session.commit()

    yield channel
