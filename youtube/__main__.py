import argparse
from pprint import pprint

from sqlalchemy.sql.expression import select

from youtube.channels import get_channel, get_channel_stats
from youtube.db import init_db


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A script that retrieves data from the YouTube API"
    )
    parser.add_argument("handles", nargs="*", help="Zero or more YouTube handles")

    args = parser.parse_args()

    # Setup database
    engine, session = init_db()

    handle = "@RickBeato"
    channel = get_channel(session, handle)
    stats = get_channel_stats(session, channel)

    print(stats)
    