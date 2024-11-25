import random

import factory
from faker import Faker as FakerLib

faker_lib = FakerLib()


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


class YouTubePlaylistItemFactory(factory.Factory):
    class Meta:
        model = dict

    kind = "youtube#playlistItem"
    etag = factory.Faker("uuid4")
    id = factory.Faker("uuid4")
    snippet = factory.LazyFunction(
        lambda: {
            "publishedAt": faker_lib.date_time().isoformat(),
            "channelId": faker_lib.uuid4(),
            "title": faker_lib.sentence(),
            "description": faker_lib.text(),
            "thumbnails": {
                "standard": {
                    "url": faker_lib.image_url(),
                    "width": 640,
                    "height": 480,
                },
            },
            "channelTitle": faker_lib.company(),
            "playlistId": faker_lib.uuid4(),
            "position": faker_lib.random_int(min=0, max=100),
            "resourceId": {
                "kind": "youtube#video",
                "videoId": faker_lib.uuid4(),
            },
        }
    )


class YouTubePlaylistResponseFactory(factory.Factory):
    class Meta:
        model = dict

    kind = "youtube#playlistItemListResponse"
    etag = factory.Faker("uuid4")
    nextPageToken = factory.Faker("uuid4")
    items = factory.List(
        [factory.SubFactory(YouTubePlaylistItemFactory) for _ in range(5)]
    )
    pageInfo = factory.LazyFunction(
        lambda: {
            "totalResults": 1966,
            "resultsPerPage": 5,
        }
    )


class YouTubeVideoStatisticsFactory(factory.Factory):
    class Meta:
        model = dict
        
    viewCount = factory.LazyFunction(
        lambda: str(random.randint(1_000, 9_999_999_999))
    )  # 10-digit number
    likeCount = factory.LazyFunction(
        lambda: str(random.randint(100, 10_000))
    )  # 7-digit number
    commentCount = factory.LazyFunction(
        lambda: str(random.randint(0, 500))
    )  # 4-digit number


class YouTubeVideoStatisticsResponseFactory(factory.Factory):
    class Meta:
        model = dict

    kind = "youtube#videoListResponse"
    etag = factory.Faker("uuid4")
    items = factory.List([factory.SubFactory(YouTubeVideoStatisticsFactory) for _ in range(5)])



class YouTubeVideoStatisticsResponseFactory(factory.Factory):
    class Meta:
        model = dict

    kind = "youtube#videoListResponse"
    etag = factory.Faker("uuid4")
    items = factory.List([factory.SubFactory(YouTubeVideoStatisticsFactory) for _ in range(5)])
