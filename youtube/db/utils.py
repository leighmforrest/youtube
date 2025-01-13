from datetime import datetime, timedelta
from sqlalchemy.orm import Session, aliased
from sqlalchemy import or_
from sqlalchemy.sql import select
from youtube.db.models import Channel, Video, VideoStats


def find_videos_with_no_or_old_stats(session: Session, channel: Channel):
    """Find videos that do not have fresh statistics."""
    one_day_ago = datetime.now() - timedelta(days=1)

    # Define an alias for VideoStats for better readability in the query
    video_stats_alias = aliased(VideoStats)

    # Query for videos with new stats (stats created within the last day)
    new_stats_query = (
        select(Video.id)  # Select only the video IDs
        .join(video_stats_alias, Video.id == video_stats_alias.video_id)
        .where(
            Video.channel_id == channel.id,
            video_stats_alias.created_at
            >= one_day_ago,  # Stats created within the last day
        )
    )

    # Find all videos with no stats or stats older than a day
    stats_query = (
        select(Video)
        .outerjoin(
            video_stats_alias, Video.id == video_stats_alias.video_id
        )  # Outer join to include all videos
        .where(
            Video.channel_id == channel.id,
            or_(
                video_stats_alias.id == None,  # No stats exist for the video
                video_stats_alias.created_at < one_day_ago,  # Stats older than a day
            ),
        )
    )

    # Exclude videos with new stats (those that have stats created within the last day)
    video_ids_with_new_stats = session.execute(new_stats_query).scalars().all()

    # Return the final query excluding videos with new stats
    return (
        session.execute(stats_query.filter(~Video.id.in_(video_ids_with_new_stats)))
        .scalars()
        .all()
    )
