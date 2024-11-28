import factory
from test.factories import fake
from test.factories.channels import ThumbnailFactory


class YouTubePlaylistItemSnippetFactory(factory.DictFactory):
    publishedAt = fake.iso8601()
    channelId = fake.uuid4()
    title = fake.sentence(nb_words=10)
    description = fake.sentence(variable_nb_words=True)
    thumbails = factory.Dict({"standard": ThumbnailFactory(width=680, height=480)})
    channel_title = fake.company()
    playlistId = fake.uuid4()
    position = fake.random_int(min=0, max=100)
    resourceId = factory.Dict({
        "kind": "youtube#video",
        "videoId": fake.uuid4()
    })


class YouTubePlaylistItemFactory(factory.DictFactory):
    kind = "youtube#playlistItem"
    etag = fake.uuid4()
    id = fake.uuid4()
    snippet = factory.SubFactory(YouTubePlaylistItemSnippetFactory)


class YouTubePlaylistResponseFactory(factory.DictFactory):
    kind = "youtube#playlistItemListResponse"
    etag = fake.uuid4()
    nextPageToken = fake.uuid4()
    items = factory.List([
        factory.SubFactory(YouTubePlaylistItemFactory) for _ in range(5)
    ])
    pageInfo = factory.Dict(
        {
            "totalResults": fake.random_int(0,1000),
            "resultsPerPage": 50,
        }
    )