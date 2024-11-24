def test_channels(youtube_channel, youtube_channel_statistics):
    assert youtube_channel["items"][0]["id"] == youtube_channel_statistics["items"][0]["id"]