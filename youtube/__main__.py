import argparse
from pprint import pprint

from sqlalchemy.sql.expression import select

from youtube.channels import get_channel, get_channel_stats
from youtube.channels_draft import (get_channel_data,
                                    sync_channel_stats_in_cache)
from youtube.db import init_db
from youtube.db.models import Base, Channel
from youtube.videos import (extract_video_ids, get_video_data,
                            get_video_statistics)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A script that retrieves data from the YouTube API"
    )
    parser.add_argument("handles", nargs="*", help="Zero or more YouTube handles")

    args = parser.parse_args()

    # Setup database
    engine, session = init_db()
    Base.metadata.create_all(engine)

    handle = "RickBeato"
    channel = get_channel(session, handle)
    stats = get_channel_stats(session, channel)
    print(stats)
    