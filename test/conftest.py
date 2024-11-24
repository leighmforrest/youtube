import pytest
from test.factories import YouTubeChannelListResponseFactory, YouTubeChannelStatisticsResponseFactory, ChannelStatisticsItemsFactory

@pytest.fixture
def youtube_channel():
    return YouTubeChannelListResponseFactory()


@pytest.fixture
def youtube_channel_statistics(youtube_channel):
   channel_id = youtube_channel["items"][0]["id"]

   return YouTubeChannelStatisticsResponseFactory(
       items=[ChannelStatisticsItemsFactory(id=channel_id)])