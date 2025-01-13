from datetime import datetime, timedelta
from sqlalchemy.orm import aliased, Session
from sqlalchemy import select

from youtube.db.models import Channel, VideoStats, Video


def find_videos_with_no_or_old_stats(session: Session, channel: Channel):
    one_day_ago = datetime.now() - timedelta(days=1)

    # define an alias for VideoStats for better readability in the query
    video_stats_alias = aliased(VideoStats)

    # query for either no VideoStats or old VideoStats
    videos_query = (
        select(Video)
        .join(video_stats_alias, Video.video_stats, isouter=True)
        .where(
            Video.channel_id == channel.id,
            (
                (video_stats_alias.id == None)
                | (video_stats_alias.created_at < one_day_ago)
            ),
        )
    )

    return session.execute(videos_query).scalars().all()
