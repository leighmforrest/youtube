import requests
from sqlalchemy.orm import Session

from youtube.db.models import Channel, ChannelStatistics
from youtube.settings import BASE_URL, YOUTUBE_KEY


def ensure_at_symbol(s: str) -> str:
    """Makes sure string s has an '@' symbol in the first character."""
    if not s.startswith("@"):
        return "@" + s
    return s


def get_channel_data_from_api(handle):
    handle = ensure_at_symbol(handle)

    channel_params = {
        "key": YOUTUBE_KEY,
        "part": "snippet,contentDetails",
        "forHandle": handle,
    }

    # Fetch channel data
    url = f"{BASE_URL}/channels"
    response = requests.get(url, channel_params)
    data = response.json()
    channel_data = data["items"][0]
    upload_playlist = channel_data["contentDetails"]["relatedPlaylists"]["uploads"]

    extracted_data = {
        "handle": handle,
        "youtube_channel_id": channel_data["id"],
        "title": channel_data["snippet"]["title"],
        "description": channel_data["snippet"]["description"],
        "thumbnail_url": channel_data["snippet"]["thumbnails"]["default"]["url"],
        "upload_playlist": upload_playlist,
    }

    return extracted_data


def get_channel_stats_from_api(channel):
    """Retrieve channel statistics from the YouTube API"""
    handle = channel.handle

    channel_params = {
        "key": YOUTUBE_KEY,
        "part": "statistics",
        "forHandle": handle,
    }

    url = f"{BASE_URL}/channels"
    response = requests.get(url, channel_params)
    data = response.json()
    statistics = data["items"][0]["statistics"]

    cleaned_statistics = {
        "channel_id": channel.id,
        "subscriber_count": int(statistics["subscriberCount"]),
        "video_count": int(statistics["videoCount"]),
        "view_count": int(statistics["viewCount"]),
    }

    return cleaned_statistics


def get_channel(session: Session, handle: str):
    """Get or create a channel in the database."""
    handle = ensure_at_symbol(handle)
    channel = Channel.get_by_handle(session, handle)

    if channel:
        print(f"Channel for {channel.handle} is in the system.")
    else:
        print("Channel is not in the system.")
        channel_data = get_channel_data_from_api(handle)
        channel = Channel(**channel_data)
        session.add(channel)
        session.commit()

    return channel


def get_channel_stats(session: Session, channel: Channel):
    print(channel)
    channel_statistics = channel.get_fresh_statistics(session)

    if channel_statistics:
        print(f"Statistics fresh for {channel.handle}")
    else:
        print(f"Statistics refreshing for {channel.handle}")

        api_channel_stats = get_channel_stats_from_api(channel)
        channel_statistics = ChannelStatistics(**api_channel_stats)
        session.add(channel_statistics)
        session.commit()

    return channel_statistics
