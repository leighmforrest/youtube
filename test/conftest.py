import json
from datetime import datetime, timedelta
from test.factories import (ChannelStatisticsItemsFactory,
                            YouTubeChannelListResponseFactory,
                            YouTubeChannelStatisticsResponseFactory,
                            YouTubeVideoStatisticsFactory,
                            YouTubeVideoStatisticsResponseFactory)
from test.helpers import generate_paginated_responses

import pytest
import requests
from sqlalchemy.orm import Session

from youtube.db import Base, init_db, sessionmaker
from youtube.db.models import Channel, ChannelStatistics
from youtube.videos import get_video_data_from_api


@pytest.fixture
def youtube_channel():
    return YouTubeChannelListResponseFactory()


@pytest.fixture
def youtube_channel_statistics(youtube_channel):
    channel_id = youtube_channel["items"][0]["id"]

    return YouTubeChannelStatisticsResponseFactory(
        items=[ChannelStatisticsItemsFactory(id=channel_id)]
    )


@pytest.fixture(scope="function")
def session():
    engine, session = init_db("sqlite:///:memory:")

    yield session

    session.rollback()
    session.close()


@pytest.fixture
def test_handle():
    return "@OurTube"


@pytest.fixture(scope="function")
def db_channel(youtube_channel, session: Session, test_handle):
    youtube_channel = youtube_channel["items"][0]

    channel_data = {
        "handle": test_handle,
        "youtube_channel_id": youtube_channel["id"],
        "title": youtube_channel["snippet"]["title"],
        "description": youtube_channel["snippet"]["description"],
        "thumbnail_url": youtube_channel["snippet"]["thumbnails"]["default"]["url"],
        "upload_playlist": youtube_channel["contentDetails"]["relatedPlaylists"][
            "uploads"
        ],
    }

    channel = Channel(**channel_data)
    session.add(channel)
    session.commit()

    yield channel


@pytest.fixture
def db_channel_stats(db_channel: Channel, session: Session, youtube_channel_statistics):
    stats = youtube_channel_statistics["items"][0]["statistics"]
    print(stats)
    statistics_data = {
        "channel_id": db_channel.id,
        "subscriber_count": stats["subscriberCount"],
        "video_count": stats["videoCount"],
        "view_count": stats["viewCount"],
    }
    channel_statistics = ChannelStatistics(**statistics_data)
    session.add(channel_statistics)
    session.commit()

    yield channel_statistics



@pytest.fixture
def db_channel_stats_stale(db_channel: Channel, session: Session, youtube_channel_statistics):
    stats = youtube_channel_statistics["items"][0]["statistics"]
    print(stats)
    
    # Create a datetime object that's more than one day ago
    one_day_ago = datetime.now() - timedelta(days=1, minutes=1)  # 2 days ago for example
    
    statistics_data = {
        "channel_id": db_channel.id,
        "subscriber_count": stats["subscriberCount"],
        "video_count": stats["videoCount"],
        "view_count": stats["viewCount"],
        "created_at": one_day_ago 
    }
    
    channel_statistics = ChannelStatistics(**statistics_data)
    
    session.add(channel_statistics)
    session.commit()

    yield channel_statistics


@pytest.fixture
def paginated_video_responses():
    return generate_paginated_responses(total_items=150, items_per_page=50)


@pytest.fixture
def mock_requests_get_videos(monkeypatch, paginated_video_responses):
    def mock_get(url, params=None, **kwargs):
        next_page_token = params.get("pageToken") if params else None

        response_data = paginated_video_responses[next_page_token]

        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps(response_data).encode("utf-8")
        return mock_response

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def videos_from_api(mock_requests_get_videos):
    return get_video_data_from_api("FakeYouTubeID")


@pytest.fixture
def mock_requests_get_video_statistics(monkeypatch):
    def mock_get(url, params=None, **kwargs):
        # Simulate response for each batch of video IDs
        video_ids = params.get("id", "").split(",")
        items = [YouTubeVideoStatisticsFactory(id=vid) for vid in video_ids]

        # Generate the response
        response_data = YouTubeVideoStatisticsResponseFactory(items=items)

        # Create a mock Response object
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps(response_data).encode("utf-8")
        return mock_response

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_requests_get_video_statistics_error(monkeypatch):
    def mock_get(url, params=None, **kwargs):
        mock_response = requests.Response()
        mock_response.status_code = 500  # Simulate server error
        return mock_response

    monkeypatch.setattr(requests, "get", mock_get)
