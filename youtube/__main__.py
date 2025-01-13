from pprint import pprint
from youtube.channels import request_channel_data, request_channel_stats
from videos import get_video_ids_from_api
from videos import get_video_data_from_api, get_video_stats_from_api
from youtube.db import init_db
from youtube.db.models import Channel, Video, ChannelStats, VideoStats
from sqlalchemy import select

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
