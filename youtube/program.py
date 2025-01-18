from sqlalchemy.orm import Session

from youtube.channels import request_channel_data, request_channel_stats
from youtube.db.models import Channel, ChannelStats
from youtube.db.utils import get_recent_channel_stats


def save_channel_stats(session: Session, channel: Channel, handle: str):
    """Helper function to fetch and save channel stats."""

    channel_stats_dict = request_channel_stats(handle)
    del channel_stats_dict["handle"]

    try:
        channel_stats = ChannelStats(**channel_stats_dict, channel=channel)
        session.add(channel_stats)
        session.commit()
    except Exception as e:
        print("EXCEPTION", e)
    return channel_stats


def get_channel_data(handle: str, session: Session):
    """Retrive channel data from database or get data from API and save it to database."""
    try:
        channel = Channel.get_by_handle(session, handle)
        channel_stats = get_recent_channel_stats(session, channel)

        if channel_stats is None:
            save_channel_stats(session, channel, handle)
        print(channel_stats)
    except ValueError:
        print("New channel, retrieving new channel data and stats")
        channel_data = request_channel_data(handle)
        channel = Channel(**channel_data)
        session.add(channel)
        session.commit()

        save_channel_stats(session, channel, handle)
    finally:
        return channel
