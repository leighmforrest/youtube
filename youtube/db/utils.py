from datetime import datetime, timedelta, timezone
from typing import List

import pandas as pd
from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql import exists, not_, select

from youtube.db.models import Channel, ChannelStats, Video, VideoStats

one_day_ago = lambda: datetime.now(timezone.utc) - timedelta(days=1)


def get_recent_channel_stats(session: Session, channel: Channel) -> ChannelStats | None:
    """Get the most recent channel stats. Will return stats less than one day old."""
    one_day_ago_time = one_day_ago()

    stmt = select(ChannelStats).where(
        ChannelStats.channel_id == channel.id,
        ChannelStats.created_at >= one_day_ago_time,
    )

    return session.execute(stmt).scalars().first()


def find_videos_with_no_or_old_stats(session: Session, channel: Channel) -> List[str]:
    """Find videos that do not have fresh statistics. Returns YouTube video IDs."""
    one_day_ago_time = one_day_ago()

    video_stats_alias = aliased(VideoStats)

    fresh_stats_subquery = select(video_stats_alias.video_id).where(
        video_stats_alias.created_at >= one_day_ago_time,
        video_stats_alias.video_id == Video.id,
    )

    query = select(Video.youtube_video_id).where(
        Video.channel_id == channel.id,
        not_(exists(fresh_stats_subquery)),  # Exclude videos with fresh stats
    )

    return list(session.execute(query).scalars().all())


def create_time_series_dataframe(session: Session, channel: Channel) -> pd.DataFrame:
    """Create a dataframe sorted by video published_at date."""
    one_day_ago_time = one_day_ago()

    stmt = (
        select(
            Channel.title.label("channel_title"),
            Video.title.label("video_title"),
            Video.youtube_video_id.label("youtube_video_id"),
            Video.published_at.label("published_at"),
            VideoStats.view_count.label("view_count"),
            VideoStats.like_count.label("like_count"),
            VideoStats.comment_count.label("comment_count"),
        )
        .join(Video, VideoStats.video_id == Video.id)
        .join(Channel, Video.channel_id == Channel.id)
        .where(VideoStats.created_at >= one_day_ago_time)
        .where(Video.channel_id == channel.id)  # Explicit foreign key reference
        .order_by(Video.published_at)
    )

    results = session.execute(stmt).fetchall()

    df = pd.DataFrame(
        results,
        columns=[
            "channel_title",
            "video_title",
            "youtube_video_id",
            "published_at",
            "view_count",
            "like_count",
            "comment_count",
        ],
    )

    df.set_index("published_at", inplace=True)
    return df
