import argparse
from pprint import pprint
from youtube.channels import get_channel_data, sync_channel_stats_in_cache
from youtube.videos import get_video_data, extract_video_ids, get_video_statistics
from youtube.db import init_db
from youtube.db.models import Base, Channel


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A script that retrieves data from the YouTube API"
    )
    parser.add_argument("handles", nargs="*", help="Zero or more YouTube handles")

    args = parser.parse_args()

    # # Setup database
    # engine, session = init_db()
    # Base.metadata.create_all(engine)

    # channel_data, statistics = get_channel_data('@MinorityMindset')

    # sync_channel_stats_in_cache(channel_data, statistics, session)
    # channel = session.query(Channel).filter(
    #     Channel.channel_id == channel_data["channel_id"]
    # ).first()

    # print(f"Channel: {channel.title} ID: {channel.channel_id} Upload Playlist: {channel.upload_playlist}")

    # for stats in channel.get_fresh_statistics(session):
    #     print(f"  Statistics for {channel.title}:")
    #     print(f"    Subscriber Count: {stats.subscriber_count}")
    #     print(f"    Video Count: {stats.video_count}")
    #     print(f"    View Count: {stats.view_count}")
    #     print(f"    Created At: {stats.created_at}")

    # session.close()
    MAX_SIZE = 50
    videos = get_video_data()
    pprint(videos)
    video_ids = extract_video_ids(videos)
    statistics = get_video_statistics(video_ids, max_batch_size=MAX_SIZE)
    print(statistics)
