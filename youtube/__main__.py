from youtube.db import init_db
from youtube.db.utils import create_time_series_dataframe, get_recent_channel_stats
from youtube.videos import get_video_ids_from_api
from youtube.program import (
    get_channel_data,
    get_video_data,
    get_video_stats,
    create_graph_from_dataframe,
)


if __name__ == "__main__":
    _, session = init_db()
    handle = "@RickBeato"

    # Get channel data and fresh stats
    print(f"Retrieving {handle}...")
    channel = get_channel_data(handle, session)

    # dipslplay latest stats for channel
    channel_stats = get_recent_channel_stats(session, channel)
    print("View Count:", channel_stats.view_count)
    print("Subscriber Count:", channel_stats.subscriber_count)
    print("Video Count:", channel_stats.video_count)

    # get video  ids for the channel
    get_video_data(channel, session)
    get_video_stats(channel, session)
    df = create_time_series_dataframe(session, channel)
    create_graph_from_dataframe(df)
