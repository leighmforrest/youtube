from channel import request_channel_data, request_channel_stats


if __name__ == "__main__":
    handle = "@RickBeato"
    channel_data = request_channel_data("@RickBeato")
    channel_stats = request_channel_stats(handle)
    print(channel_data)
    print(channel_stats)
