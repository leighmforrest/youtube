from youtube.db import init_db
from youtube.program import get_channel_data


if __name__ == "__main__":
    _, session = init_db()
    handle = "@RickBeato"

    # Get channel data and fresh stats
    print(f"Retrieving {handle}...")
    channel_data = get_channel_data(handle, session)
    print(channel_data.channel_stats[0])
