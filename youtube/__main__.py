from channel import request_channel_data


if __name__ == "__main__":
    handle = "@RickBeato"
    channel_data = request_channel_data("@RickBeato")
    print(channel_data)
