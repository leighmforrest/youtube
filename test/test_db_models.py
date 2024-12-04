from datetime import datetime, timedelta, timezone
from test import test_session

import pytest
from sqlalchemy.orm import Session

from youtube.db.models import Channel


def test_channel_instance(testing_channel):
    assert testing_channel is not None
    assert testing_channel.youtube_channel_id is not None

    assert isinstance(testing_channel.created_at, datetime)
    created_at_aware = testing_channel.created_at.replace(tzinfo=timezone.utc)
    assert created_at_aware <= datetime.now(timezone.utc)

    assert isinstance(testing_channel.id, int)


def test_channel_with_videos(testing_videos_for_channel, testing_channel):

    assert len(testing_channel.videos) == 5


def test_channel___str__(testing_channel):
    assert str(testing_channel) == f"<Channel: {testing_channel.handle}>"


def test_get_channel_by_handle(testing_channel):
    handle = testing_channel.handle
    result = Channel.get_by_handle(test_session, handle)

    assert result == testing_channel
    assert result.handle[0] == "@"


def test_get_channel_by_handle_fail(testing_channel):
    handle = "FakeYoutubeChannel"
    error_string = f"Channel with handle '{handle}' not found."
    with pytest.raises(ValueError, match=error_string):
        Channel.get_by_handle(test_session, handle=handle)


def test_video_instance(testing_videos_for_channel, testing_channel):
    assert len(testing_videos_for_channel) == 5

    for video in testing_videos_for_channel:
        assert isinstance(video.id, int)
        assert isinstance(video.thumbnail_url, str)
        assert isinstance(video.title, str)
        assert video.channel == testing_channel
        assert video.channel_id == testing_channel.id
        assert isinstance(video.published_at, datetime)


def test_channel_with_old_timestamp(testing_channel_with_old_date):
    assert testing_channel_with_old_date.created_at < (
        datetime.now() - timedelta(days=2)
    )


def test_channel_with_current_timestamp(testing_channel):
    assert testing_channel.created_at != (datetime.now() - timedelta(days=2))


def test_channel_without_stats(testing_channel):
    assert testing_channel.statistics is None


def test_channel_with_stats(testing_channel, testing_channel_with_stats):
    assert testing_channel.statistics.channel == testing_channel
