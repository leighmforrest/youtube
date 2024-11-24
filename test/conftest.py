import pytest
from sqlalchemy.orm import Session
from youtube.db import init_db, Base, sessionmaker
from youtube.db.models import Channel, ChannelStatistics
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
        "view_count": stats["viewCount"]
    }
    channel_statistics = ChannelStatistics(**statistics_data)
    session.add(channel_statistics)
    session.commit()

    yield channel_statistics