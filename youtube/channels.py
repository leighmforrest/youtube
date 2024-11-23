import requests
from pprint import pprint
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from youtube.db.utils import get_or_create
from youtube.db.models import Channel, ChannelStatistics
from settings import YOUTUBE_KEY, BASE_URL


one_day_ago = datetime.now(timezone.utc) - timedelta(days=1)


def get_channel_data(handle="@RickBeato"):
    """Retrieve channel data from the api."""

    channel_params = {
        "key": YOUTUBE_KEY,
        "part": "snippet,statistics,contentDetails",
        "forHandle": handle,
    }

    # Fetch channel data
    url = f"{BASE_URL}/channels"
    response = requests.get(url, channel_params)
    data = response.json()
    channel_data = data["items"][0]

    # Extract the upload playlist id
    upload_playlist = channel_data["contentDetails"]["relatedPlaylists"]["uploads"]
    print("UPLOAD PLAYLIST", upload_playlist)

    extracted_data = {
        "channel_id": channel_data["id"],
        "title": channel_data["snippet"]["title"],
        "description": channel_data["snippet"]["description"],
        "thumbnail_url": channel_data["snippet"]["thumbnails"]["default"]["url"],
        "upload_playlist": upload_playlist,
    }

    # Remove hiddenSubscriber count from statistics
    statistics = channel_data["statistics"]
    print(statistics)
    del statistics["hiddenSubscriberCount"]

    cleaned_statistics = {
        "subscriber_count": statistics["subscriberCount"],
        "video_count": statistics["videoCount"],
        "view_count": statistics["viewCount"],
    }

    return extracted_data, cleaned_statistics


def sync_channel_stats_in_cache(channel_data: dict, statistics: dict, session: Session):
    """Get or create the cache and get fresh (less than one day old) statistics."""
    channel, created = get_or_create(session, Channel, **channel_data)

    if created:
        print("Channel has been created.")
    else:
        print("Channel is in the cache.")

    recent_statistics_query = session.query(ChannelStatistics).filter(
        ChannelStatistics.channel_id == channel.id,
        ChannelStatistics.created_at >= one_day_ago,
    )

    if not recent_statistics_query.first():
        print("Cache miss: creating new channel statistics.")
        new_statistics = ChannelStatistics(channel_id=channel.id, **statistics)
        session.add(new_statistics)
        session.commit()
    else:
        print("Cache hit: statistics are in the cache.")
