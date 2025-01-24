from youtube.db import init_db
from youtube.videos import get_video_ids_from_api
from youtube.program import get_channel_data, get_video_data, get_video_stats


if __name__ == "__main__":
    _, session = init_db()
    handle = "@RickBeato"

    # Get channel data and fresh stats
    print(f"Retrieving {handle}...")
    channel = get_channel_data(handle, session)

    # get video  ids for the channel
    get_video_data(channel, session)
    get_video_stats(channel, session)
