from test.factories import fake

import factory


class ThumbnailFactory(factory.DictFactory):
    url = fake.image_url()
    width = 88
    height = 88


class SnippetFactory(factory.DictFactory):
    title = fake.name()
    description = fake.sentence(nb_words=7)
    thumbnails = factory.Dict({"default": ThumbnailFactory()})


class ContentDetailsFactory(factory.DictFactory):
    relatedPlaylists = {"uploads": fake.uuid4()}


class ItemsFactory(factory.DictFactory):
    etag = fake.uuid4()
    id = fake.uuid4()
    snippet = factory.SubFactory(SnippetFactory)
    contentDetails = factory.SubFactory(ContentDetailsFactory)


class YouTubeChannelListResponseFactory(factory.DictFactory):
    kind = "youtube#channelListResponse"
    etag = factory.Faker("uuid4")
    items = factory.List([ItemsFactory()])


class YouTubeChannelStatisticsFactory(factory.DictFactory):
    viewCount = fake.random_int(min=1, max=1_000_000_000)
    subscriberCount = fake.random_int(min=1, max=1_000_000_000)
    videoCount = fake.random_int(min=0, max=1_000_000_000)


class YouTubeChannelStatisticsItemsFactory(factory.DictFactory):
    etag = fake.uuid4()
    id = fake.uuid4()
    statistics = factory.SubFactory(YouTubeChannelStatisticsFactory)


class YouTubeChannelStatisticsResponseFactory(factory.DictFactory):
    kind = "youtube#channelListResponse"
    etag = fake.uuid4()
    items = factory.List([YouTubeChannelStatisticsItemsFactory()])
