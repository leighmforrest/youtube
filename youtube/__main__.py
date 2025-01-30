import argparse

from youtube.db import init_db
from youtube.db.utils import (create_time_series_dataframe,
                              get_recent_channel_stats)
from youtube.program import (create_graph_from_dataframe,
                             display_channel_stats,
                             display_stats_from_dataframe, get_channel_data,
                             get_video_data, get_video_stats, save_to_csv)
from youtube.settings import BASE_DIR
from youtube.utils import add_at_symbol, remove_at_symbol

parser = argparse.ArgumentParser(
    prog="YouTube",
    description="Program to retrieve statistics from the YouTube API",
    epilog="Text at the bottom of help",
)


if __name__ == "__main__":
    parser.add_argument("handle")
    args = parser.parse_args()
    handle = add_at_symbol(args.handle)
    channel_name = remove_at_symbol(handle)

    # set up db
    _, session = init_db()

    try:
        # Get channel data and fresh stats
        print(f"Retrieving {handle}...")
        channel = get_channel_data(handle, session)

        # get video  ids for the channel
        get_video_data(channel, session)
        get_video_stats(channel, session)
        df = create_time_series_dataframe(session, channel)

        # Display channel stats
        display_channel_stats(session, channel)
        # Display stats from dataframe
        display_stats_from_dataframe(df)

        # Display graphs on the screen
        create_graph_from_dataframe(df, metric="view_count")
        create_graph_from_dataframe(df, metric="comment_count")
        create_graph_from_dataframe(df, metric="like_count")

        # Save to csv
        print("Now saving data to the directory...")
        save_to_csv(df, BASE_DIR / f"{channel_name}.csv")
    except Exception as e:
        print("The channel could not be found.")
        print("ERROR:", e)
