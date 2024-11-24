import pytest
from youtube.db import init_db, Base, sessionmaker
from youtube.db.models import Channel
from test.factories import (
    YouTubeChannelListResponseFactory,
    YouTubeChannelStatisticsResponseFactory,
    ChannelStatisticsItemsFactory,
)


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
def db_channel(youtube_channel, session, test_handle):
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
