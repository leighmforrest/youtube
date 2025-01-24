from sqlalchemy.orm import Session
from sqlalchemy import select

from youtube.channels import request_channel_data, request_channel_stats
from youtube.videos import (
    get_video_ids_from_api,
    get_video_data_from_api,
    get_video_stats_from_api,
)
from youtube.db.models import Channel, ChannelStats, Video, VideoStats
from youtube.db.utils import get_recent_channel_stats, find_videos_with_no_or_old_stats


def save_channel_stats(session: Session, channel: Channel, handle: str):
    """Helper function to fetch and save channel stats."""
    try:
        channel_stats_dict = request_channel_stats(handle)
        del channel_stats_dict["handle"]

        channel_stats = ChannelStats(**channel_stats_dict, channel=channel)
        session.add(channel_stats)
        session.commit()
        return channel_stats
    except Exception as e:
        session.rollback()  # Rollback on failure
        print("EXCEPTION in save_channel_stats:", e)
        return None


def get_video_ids_not_in_database(api_video_ids, session: Session):
    """Identify video IDs not stored in the database."""
    api_video_id_set = set(api_video_ids)

    # Retrieve existing video IDs from the database
    stmt = select(Video.youtube_video_id).where(
        Video.youtube_video_id.in_(api_video_ids)
    )
    saved_video_id_set = {row[0] for row in session.execute(stmt)}

    # Return the difference
    return list(api_video_id_set - saved_video_id_set)


def get_channel_data(handle: str, session: Session):
    """Retrieve or fetch and save channel data."""
    try:
        # Try to fetch the channel by handle
        channel = Channel.get_by_handle(session, handle)
        channel_stats = get_recent_channel_stats(session, channel)

        if channel_stats is None:
            print(f"Updating stats for channel: {handle}")
            save_channel_stats(session, channel, handle)
        else:
            print(f"Recent stats already exist for channel: {handle}")
    except ValueError:
        # Handle new channel creation
        print(f"New channel detected: {handle}. Fetching from API...")
        channel_data = request_channel_data(handle)
        channel = Channel(**channel_data)
        session.add(channel)
        session.commit()
        save_channel_stats(session, channel, handle)

    return channel


def get_video_data(channel: Channel, session: Session):
    """Save unsaved videos and stats for a channel."""
    video_objects = []
    video_ids = get_video_ids_from_api(channel.uploads_playlist)
    unsaved_video_ids = get_video_ids_not_in_database(video_ids, session)

    if not unsaved_video_ids:
        print("All videos are already saved in the database.")
        return

    print(f"Found {len(unsaved_video_ids)} new videos to save.")

    unsaved_video_data = get_video_data_from_api(unsaved_video_ids)

    for video_data, video_stats_dict in unsaved_video_data:
        # Remove youtube_video_id from stats
        del video_stats_dict["youtube_video_id"]

        # Save video and stats in one transaction
        video = Video(**video_data, channel=channel)
        session.add(video)

        video_stats = VideoStats(**video_stats_dict, video=video)
        session.add(video_stats)

    session.commit()  # Commit after adding all videos and stats
    print(f"Saved {len(unsaved_video_ids)} new videos.")


def get_video_stats(channel: Channel, session: Session):
    """Check and update stats for videos."""
    youtube_video_ids = find_videos_with_no_or_old_stats(session, channel)

    if not youtube_video_ids:
        print("All videos have up-to-date stats.")
    else:
        print(f"{len(youtube_video_ids)} videos need updated stats.")

        video_stats_objects = []
        video_stats = get_video_stats_from_api(youtube_video_ids)

        # save video stats to database
        for video_stats_dict in video_stats:
            print(video_stats_dict)
            youtube_video_id = video_stats_dict["youtube_video_id"]
            del video_stats_dict["youtube_video_id"]

            video = Video.get_by_youtube_video_id(session, youtube_video_id)
            print(video)
            video_stats_objects.append(VideoStats(**video_stats_dict, video=video))

        session.add_all(video_stats_objects)
        session.commit()

        print(f"Saved {len(video_stats_objects)} to database.")
