import random
import factory


class ThumbnailFactory(factory.DictFactory):
    url = factory.Faker("image_url")
    width = 88
    height = 88


class SnippetFactory(factory.DictFactory):
    title = factory.Faker("name")
    description = factory.Faker("sentence")
    thumbnails = factory.Dict({"default": ThumbnailFactory.build()})


class ContentDetailsFactory(factory.DictFactory):
    relatedPlaylists = factory.Dict({"uploads": factory.Faker("uuid4")})


class ItemsFactory(factory.DictFactory):
    etag = factory.Faker("uuid4")
    id = factory.Faker("uuid4")
    snippet = factory.SubFactory(SnippetFactory)
    contentDetails = factory.SubFactory(ContentDetailsFactory)


class YouTubeChannelListResponseFactory(factory.DictFactory):
    kind = "youtube#channelListResponse"
    etag = factory.Faker("uuid4")
    items = factory.List([factory.SubFactory(ItemsFactory)])


class StatisticsFactory(factory.DictFactory):
    viewCount = factory.LazyFunction(
        lambda: str(random.randint(1_000_000_000, 9_999_999_999))
    )  # 10-digit number
    subscriberCount = factory.LazyFunction(
        lambda: str(random.randint(1_000_000, 9_999_999))
    )  # 7-digit number
    hiddenSubscriberCount = False
    videoCount = factory.LazyFunction(
        lambda: str(random.randint(1_000, 9_999))
    )  # 4-digit number


class ChannelStatisticsItemsFactory(factory.DictFactory):
    etag = factory.Faker("uuid4")
    id = factory.Faker("uuid4")
    snippet = factory.SubFactory(SnippetFactory)
    statistics = factory.SubFactory(StatisticsFactory)


class YouTubeChannelStatisticsResponseFactory(factory.DictFactory):
    kind = "youtube#channelListResponse"
    etag = factory.Faker("uuid4")
    items = factory.List([factory.SubFactory(ChannelStatisticsItemsFactory)])
