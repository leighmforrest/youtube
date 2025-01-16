import pytest
from datetime import datetime
from youtube.db.models import Channel, Video, VideoStats, ChannelStats
from youtube.db.utils import find_videos_with_no_or_old_stats


class TestChannel:
    def test_channel_exists(self, test_channel):
        assert isinstance(test_channel, Channel)
        assert isinstance(test_channel.id, int)
        assert len(test_channel.title) > 0
        assert len(test_channel.description) > 0
        assert len(test_channel.youtube_channel_id) > 0
        assert len(test_channel.thumbnail_url) > 0
        assert len(test_channel.uploads_playlist) > 0

    def test_channel____str__(self, test_channel):
        assert str(test_channel) == f"<Channel: {test_channel.handle}>"

    def test_related_videos(self, test_channel: Channel, test_five_videos):
        assert len(test_channel.videos) == 5

    def test_get_by_handle_success(self, test_channel, test_handle, test_session):
        result = Channel.get_by_handle(test_session, test_handle)
        assert result == test_channel

    @pytest.mark.parametrize("handle", ["@fakeName", "@RickBeeto", "@PewDEPye"])
    def test_get_by_handle_fail(self, test_channel, test_session, handle):
        with pytest.raises(ValueError):
            result = Channel.get_by_handle(test_session, handle)
            assert result is None


class TestVideos:
    def test_videos_exist(self, test_channel, test_five_videos):
        for video in test_channel.videos:
            assert isinstance(video, Video)
            assert isinstance(video.published_at, datetime)
            assert isinstance(video.duration, int)
            assert len(video.youtube_video_id) > 0
            assert len(video.description) > 0
            assert len(video.title) > 0
            assert len(video.thumbnail_url) > 0
            assert video.channel == test_channel

    def test___str__(self, test_five_videos):
        for video in test_five_videos:
            assert str(video) == f"<Video: {video.title}>"

    def test_get_by_youtube_id_success(self, test_five_videos, test_session):
        for video in test_five_videos:
            youtube_video_id = video.youtube_video_id
            result = Video.get_by_youtube_video_id(test_session, youtube_video_id)
            assert result == video

    @pytest.mark.parametrize(
        "video_id",
        ["UVVVsdfsdfe", "HAHAHHAHAAAA", "UVVVV1234455555", "ABDCD1232323123"],
    )
    def test_get_by_youtube_id_fail(self, test_session, video_id):
        with pytest.raises(ValueError):
            result = Video.get_by_youtube_video_id(test_session, video_id)
            assert result is None


class TestVideoStats:
    def test_video_stats_exist(self, test_five_videos_stats_current, test_five_videos):
        for video in test_five_videos:
            video_stats = video.video_stats[0]
            assert isinstance(video_stats, VideoStats)
            assert isinstance(video_stats.id, int)
            assert isinstance(video_stats.view_count, int)
            assert isinstance(video_stats.like_count, int)
            assert isinstance(video_stats.comment_count, int)
            assert isinstance(video_stats.favorite_count, int)

    def test_video_stats___str__(self, test_five_videos_stats_current):
        for video_stats in test_five_videos_stats_current:
            assert str(video_stats) == f"<VideoStats: {video_stats.video.title}>"


class TestChannelStats:
    def test_channel_stats_exist(
        self, test_channel_stats: ChannelStats, test_channel: Channel
    ):
        assert test_channel_stats.channel == test_channel
        assert test_channel_stats.video_count >= 0
        assert test_channel_stats.view_count >= 0
        assert test_channel_stats.subscriber_count >= 0

    def test_channel_stats___str__(self, test_channel_stats):
        assert (
            str(test_channel_stats)
            == f"<ChannelStats: {test_channel_stats.channel.handle}>"
        )
