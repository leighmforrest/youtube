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
    print(test_channel.videos)


def test_channel___str__(test_channel: Channel):
    assert str(test_channel) == f"<Channel: {test_channel.handle}>"


def test_get_channel_by_handle(test_channel: Channel, test_session: Session):
    handle = test_channel.handle
    result = Channel.get_by_handle(test_session, handle)

    assert result == test_channel
