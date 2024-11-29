from test.factories import fake
from test.factories.channels import ThumbnailFactory

import factory


class YouTubePlaylistItemSnippetFactory(factory.DictFactory):
    publishedAt = factory.Faker("iso8601")
    channelId = factory.Faker("uuid4")
    title = factory.Faker("sentence", nb_words=10)
    description = factory.Faker("sentence", variable_nb_words=True)
    thumbnails = factory.LazyAttribute(
        lambda _: {"standard": ThumbnailFactory(width=680, height=480)}
    )
    channel_title = factory.Faker("company")
    playlistId = factory.Faker("uuid4")
    position = factory.Faker("random_int", min=0, max=100)
    resourceId = factory.LazyAttribute(
        lambda _: {"kind": "youtube#video", "videoId": fake.uuid4()}
    )


class YouTubePlaylistItemFactory(factory.DictFactory):
    kind = "youtube#playlistItem"
    etag = factory.Faker("uuid4")
    id = factory.Faker("uuid4")
    snippet = factory.SubFactory(YouTubePlaylistItemSnippetFactory)


class YouTubePlaylistResponseFactory(factory.DictFactory):
    kind = "youtube#playlistItemListResponse"
    etag = factory.Faker("uuid4")
    nextPageToken = factory.Faker("uuid4")
    items = factory.LazyAttribute(
        lambda _: [YouTubePlaylistItemFactory() for _ in range(5)]
    )
    pageInfo = factory.LazyAttribute(
        lambda _: {
            "totalResults": fake.random_int(0, 1000),
            "resultsPerPage": 50,
        }
    )


class YouTubeVideoStatisticsFactory(factory.DictFactory):
    viewCount = factory.Faker("random_int", min=100, max=1_000_000_000)
    likeCount = factory.Faker("random_int", min=1, max=1_000_000_000)
    commentCount = factory.Faker("random_int", min=0, max=1000)


class YouTubeVideoStatisticsItemFactory(factory.DictFactory):
    kind = "youtube#video"
    etag = factory.Faker("uuid4")
    id = factory.Faker("uuid4")
    statistics = factory.SubFactory(YouTubeVideoStatisticsFactory)


class YouTubeVideoStatisticsResponseFactory(factory.DictFactory):
    kind = "youtube#videoListResponse"
    etag = factory.Faker("uuid4")
    items = factory.LazyAttribute(
        lambda _: [YouTubeVideoStatisticsItemFactory() for _ in range(5)]
    )
    pageInfo = factory.Dict(
        {
            "totalResults": 3,
            "resultsPerPage": 3,
        }
    )
