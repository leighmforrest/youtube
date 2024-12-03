import pytest
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from youtube.db.models import Channel


def test_channel_instance(test_channel: Channel):
    assert test_channel is not None
    assert test_channel.youtube_channel_id is not None

    assert isinstance(test_channel.created_at, datetime)
    created_at_aware = test_channel.created_at.replace(tzinfo=timezone.utc)
    assert created_at_aware <= datetime.now(timezone.utc)

    assert isinstance(test_channel.id, int)


def test_channel___str__(test_channel: Channel):
    assert str(test_channel) == f"<Channel: {test_channel.handle}>"


def test_get_channel_by_handle(test_channel: Channel, test_session: Session):
    handle = test_channel.handle
    result = Channel.get_by_handle(test_session, handle)

    assert result == test_channel


def test_get_channel_by_handle_fail(test_channel: Channel, test_session: Session):
    handle = "FakeYoutubeChannel"
    error_string = f"Channel with handle '{handle}' not found."
    with pytest.raises(ValueError, match=error_string):
        Channel.get_by_handle(test_session, handle=handle)


def test_video_instance(test_channel: Channel):
    videos = test_channel.videos

    assert len(videos) == 6
    
    for video in videos:
        assert isinstance(video.id, int)
        assert isinstance(video.thumbnail_url, str)
        assert isinstance(video.title, str)
        assert video.channel == test_channel
        assert video.channel_id == test_channel.id
        assert isinstance(video.published_at, datetime)
