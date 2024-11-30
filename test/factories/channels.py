from datetime import datetime, timezone
from test.factories import fake

import factory
from sqlalchemy.orm import Session

from youtube.db.models import Channel, Video


class ThumbnailFactory(factory.DictFactory):
    url = factory.LazyAttribute(lambda _: fake.image_url())
    width = factory.LazyFunction(lambda: fake.random_int(min=50, max=200))
    height = factory.LazyFunction(lambda: fake.random_int(min=50, max=200))


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


###
# Database Factories
#
# The testing Session is to be used. Just add the parent in most cases when building.
###
class ChannelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Channel
        sqlalchemy_session = Session

    youtube_channel_id = factory.LazyFunction(fake.uuid4)
    title = factory.LazyAttribute(lambda _: fake.name())
    description = factory.LazyAttribute(lambda _: fake.sentence(nb_words=7))
    handle = factory.LazyAttribute(lambda _: f"@{fake.user_name()}")
    upload_playlist = factory.LazyFunction(fake.uuid4)
    thumbnail_url = factory.LazyAttribute(lambda _: fake.image_url())

    videos = factory.RelatedFactoryList(
        "test.factories.channels.VideoFactory", factory_related_name="channel", size=3
    )


class VideoFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Video
        sqlalchemy_session = Session

    video_id = factory.Faker("uuid4")
    thumbnail_url = factory.Faker("image_url")
    title = factory.Faker("sentence")
    published_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))

    # Relationship to Channel
    channel = factory.SubFactory(ChannelFactory)


class ChannelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Channel
        sqlalchemy_session = Session  # Replace with your test session

    youtube_channel_id = factory.Faker("uuid4")
    title = factory.Faker("company")
    description = factory.Faker("sentence", nb_words=7)
    handle = factory.LazyAttribute(lambda _: f"@{fake.user_name()}")
    upload_playlist = factory.Faker("uuid4")
    thumbnail_url = factory.Faker("image_url")

    # Relationship: Videos associated with this Channel
    videos = factory.RelatedFactoryList(
        "test.factories.videos.VideoFactory", factory_related_name="channel", size=3
    )
