from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql import not_
from sqlalchemy.sql import select, exists
from youtube.db.models import Channel, Video, VideoStats, ChannelStats


one_day_ago = lambda: datetime.now(timezone.utc) - timedelta(days=1)


def get_recent_channel_stats(session: Session, channel: Channel):
    """Get the most recent channel stats. Will return stats less than one day old."""
    one_day_ago_time = one_day_ago()

    stmt = select(ChannelStats).where(
        ChannelStats.channel_id == channel.id,
        ChannelStats.created_at >= one_day_ago_time,
    )

    result = session.execute(stmt).scalars().first()

    return result


def find_videos_with_no_or_old_stats(session: Session, channel: Channel):
    """Find videos that do not have fresh statistics. Returns YouTube video IDs."""
    one_day_ago_time = one_day_ago()

    # Alias for VideoStats
    video_stats_alias = aliased(VideoStats)

    # Subquery: Videos with fresh stats
    fresh_stats_subquery = select(video_stats_alias.video_id).where(
        video_stats_alias.created_at >= one_day_ago_time,
        video_stats_alias.video_id == Video.id,
    )

    # Main Query: Videos with no fresh stats
    query = select(Video.youtube_video_id).where(
        Video.channel_id == channel.id,
        not_(exists(fresh_stats_subquery)),  # Exclude videos with fresh stats
    )

    # Execute and return results
    result = session.execute(query).scalars().all()
    return result
