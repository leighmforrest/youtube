from pprint import pprint
from datetime import datetime, timedelta
from youtube.channels import request_channel_data, request_channel_stats
from videos import get_video_ids_from_api
from videos import get_video_data_from_api, get_video_stats_from_api
from youtube.db import init_db
from youtube.db.models import Channel, Video, ChannelStats, VideoStats
from youtube.db.utils import find_videos_with_no_or_old_stats
from sqlalchemy import select, func

yesterday_and_ten_seconds = datetime.now() - timedelta(days=1, seconds=10)

if __name__ == "__main__":
    _, session = init_db()
    handle = "@RickBeato"
    channel_data = request_channel_data(handle)
    channel = Channel(**channel_data)
    session.add(channel)
    session.commit()

    channel = Channel.get_by_handle(session, handle)
    print("SAVED CHANNEL ID", channel.id)
    print("SAVED YOUTUBE ID", channel.youtube_channel_id)

    # get channel stats
    channel_stats_dict = request_channel_stats(channel.handle)
    del channel_stats_dict["handle"]
    channel_stats = ChannelStats(**channel_stats_dict, channel=channel)
    session.add(channel_stats)
    session.commit()

    print(channel.channel_stats[0].subscriber_count)
    print(channel.channel_stats[0].video_count)
    print(channel.channel_stats[0].view_count)

    # get youtube video ids
    playlist_id = channel.uploads_playlist
    video_ids = get_video_ids_from_api(playlist_id)
    video_data_tuples = get_video_data_from_api(video_ids)

    # Add videos to database
    for video_tuple in video_data_tuples:
        video_data = video_tuple[0]
        video_stats = video_tuple[1]
        del video_stats["youtube_video_id"]
        video = Video(**video_data, channel=channel)
        video_stats = VideoStats(**video_stats, video=video)
        session.add(video)
        session.add(video_stats)
        session.commit()

    # display video data
    stmt = select(VideoStats)
    videos = session.scalars(stmt).all()

    for vid in videos:
        print(f"{vid.view_count}")

    # pick 25 video_stats rows at random
    stmt = select(VideoStats).order_by(func.random()).limit(25)
    results = session.scalars(stmt).all()

    for row in results:
        row.created_at = yesterday_and_ten_seconds
        session.add(row)
        session.commit()

    videos = find_videos_with_no_or_old_stats(session, channel)
    print(f"The number of videos with stale stats is {len(videos)}")
    old_video_ids = [video.youtube_video_id for video in videos]
    new_video_stats = get_video_stats_from_api(old_video_ids)

    # for every new video stat
    for new_video_stats_dict in new_video_stats:
        # get video by id
        video = Video.get_by_youtube_video_id(
            session, new_video_stats_dict["youtube_video_id"]
        )
        # delete youtube_video_id in dict
        del new_video_stats_dict["youtube_video_id"]
        # save new stats to database
        video_stats = VideoStats(**new_video_stats_dict, video=video)
        session.add(video_stats)
        session.commit()

    videos = find_videos_with_no_or_old_stats(session, channel)
    print(f"The number of videos with stale stats is {len(videos)}")

    session.close()
