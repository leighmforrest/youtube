from datetime import datetime, timezone
from test import test_session
from test.factories import ThumbnailFactory, fake

import factory
import factory.fuzzy
from sqlalchemy.orm import Session

from youtube.db.models import Channel, ChannelStats, Video


class SnippetFactory(factory.DictFactory):
    title = factory.LazyAttribute(lambda _: fake.name())
    description = factory.LazyAttribute(lambda _: fake.sentence(nb_words=7))
    thumbnails = factory.Dict({"default": factory.SubFactory(ThumbnailFactory)})


class ContentDetailsFactory(factory.DictFactory):
    relatedPlaylists = factory.Dict({"uploads": factory.LazyFunction(fake.uuid4)})


class ItemsFactory(factory.DictFactory):
    etag = factory.LazyFunction(fake.uuid4)
    id = factory.LazyFunction(fake.uuid4)
    snippet = factory.SubFactory(SnippetFactory)
    contentDetails = factory.SubFactory(ContentDetailsFactory)


class YouTubeChannelListResponseFactory(factory.DictFactory):
    kind = "youtube#channelListResponse"
    etag = factory.LazyFunction(fake.uuid4)
    items = factory.List(
        [factory.SubFactory(ItemsFactory) for _ in range(3)]
    )  # Example with 3 items


class YouTubeChannelStatisticsFactory(factory.DictFactory):
    viewCount = factory.LazyFunction(lambda: fake.random_int(min=1, max=1_000_000_000))
    subscriberCount = factory.LazyFunction(
        lambda: fake.random_int(min=1, max=1_000_000_000)
    )
    videoCount = factory.LazyFunction(lambda: fake.random_int(min=0, max=1_000_000_000))


class YouTubeChannelStatisticsItemsFactory(factory.DictFactory):
    etag = factory.LazyFunction(fake.uuid4)
    id = factory.LazyFunction(fake.uuid4)
    statistics = factory.SubFactory(YouTubeChannelStatisticsFactory)


class YouTubeChannelStatisticsResponseFactory(factory.DictFactory):
    kind = "youtube#channelListResponse"
    etag = factory.LazyFunction(fake.uuid4)
    items = factory.List(
        [factory.SubFactory(YouTubeChannelStatisticsItemsFactory) for _ in range(3)]
    )


##
# DB Factories
##
class DBChannelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Channel
        sqlalchemy_session = test_session
        sqlalchemy_session_persistence = "commit"

    title = factory.LazyFunction(fake.name)
    description = factory.LazyFunction(fake.sentence)
    handle = factory.LazyAttribute(lambda obj: f"@{fake.user_name()}")
    upload_playlist = factory.LazyFunction(fake.uuid4)
    youtube_channel_id = factory.LazyFunction(fake.uuid4)
    thumbnail_url = factory.Faker("image_url")


class DBVideoFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Video
        sqlalchemy_session = test_session
        sqlalchemy_session_persistence = "commit"

    thumbnail_url = factory.LazyFunction(fake.image_url)
    title = factory.LazyFunction(fake.sentence)
    published_at = factory.LazyFunction(fake.date_time_this_year)
    video_id = factory.LazyFunction(fake.uuid4)
    channel = factory.SubFactory(DBChannelFactory)


class DBChannelStatsFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ChannelStats
        sqlalchemy_session = test_session
        sqlalchemy_session_persistence = "commit"

    view_count = factory.LazyFunction(lambda: fake.random_int(min=1, max=1_000_000_000))
    subscriber_count = factory.LazyFunction(
        lambda: fake.random_int(min=1, max=1_000_000_000)
    )
    video_count = factory.LazyFunction(
        lambda: fake.random_int(min=0, max=1_000_000_000)
    )
    channel = factory.SubFactory(DBChannelFactory)
