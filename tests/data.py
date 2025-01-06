from faker import Faker


fake = Faker()


# Quick function to generate a random published at date
published_at = (
    lambda: fake.date_time_between("-10y", "now").isoformat(sep="T", timespec="seconds")
    + "Z"
)


##
#   Mock Youtube API 200 requests
##
def mock_channels_list_api_data(handle):
    """Mock data from a request from channelsList api endpoint."""
    return {
        "kind": "youtube#channelListResponse",
        "etag": fake.md5(raw_output=False),
        "pageInfo": {"totalResults": 1, "resultsPerPage": 5},
        "items": [
            {
                "kind": "youtube#channel",
                "etag": fake.md5(raw_output=False),
                "id": fake.lexify("UC????????????????????"),
                "snippet": {
                    "title": fake.name(),
                    "description": fake.sentence(nb_words=3),
                    "publishedAt": published_at(),
                    "thumbnails": {"default": {"url": fake.image_url()}},
                },
                "contentDetails": {
                    "relatedPlaylists": {
                        "uploads": fake.lexify(
                            "UU????????????????????"
                        )  # 24-character playlist ID
                    }
                },
            }
        ],
    }


def mock_channels_list_api_stats(handle):
    return {
        "kind": "youtube#channelListResponse",
        "etag": fake.md5(raw_output=False),
        "pageInfo": {"totalResults": 1, "resultsPerPage": 5},
        "items": [
            {
                "kind": "youtube#channel",
                "etag": fake.md5(raw_output=False),
                "id": fake.lexify("UC????????????????????"),
                "statistics": {
                    "viewCount": str(fake.random_int(0, 1_000_000_000)),
                    "subscriberCount": str(fake.random_int(0, 1_000_000_000)),
                    "videoCount": str(fake.random_int(0, 1000)),
                    "hiddenSubscriberCount": fake.boolean(),
                },
            }
        ],
    }


def mock_request_playlist_items_api_item(video_id=None):
    """Generate a single playlist item."""
    return {
        "kind": "youtube#playlistItem",
        "etag": fake.md5(raw_output=False),
        "id": fake.lexify("VVUKc??????"),
        "contentDetails": {
            "videoId": video_id or fake.lexify("???????"),
            "videoPublishedAt": published_at(),
        },
    }


def mock_request_playlist_items_api_paginated_dictionary(
    total_pages=3, items_per_page=50
):
    """Generate the playlist item pages in dictionary form."""
    total_items = total_pages * items_per_page
    # Generate all unique items
    all_items = [mock_request_playlist_items_api_item() for _ in range(total_items)]
    responses = {}

    for page in range(total_pages):
        start_idx = page * items_per_page
        end_idx = start_idx + items_per_page
        page_items = all_items[start_idx:end_idx]

        # Generate nextPageToken if there is another page
        next_page_token = f"Page_{page+1}" if page + 1 < total_pages else None

        # Create the response for the current page
        responses[f"Page_{page}"] = {
            "kind": "youtube#playlistItemListResponse",
            "etag": fake.md5(raw_output=False),
            "nextPageToken": next_page_token,
            "items": page_items,
            "pageInfo": {
                "totalResults": total_items,
                "resultsPerPage": items_per_page,
            },
        }

    return responses


##
#   Mock extracted data
##
def mock_request_channel_data(handle):
    """Use to mock the output of request_channel_data()"""
    return {
        "handle": handle,
        "youtube_channel_id": fake.lexify("UC????????????????????"),
        "title": fake.name(),
        "description": fake.sentence(nb_words=3),
        "thumbnail_url": fake.image_url(),
        "uploads_playlist": fake.lexify("UU????????????????????"),
    }


def mock_request_channel_stats(handle):
    """Use to mock the output of request_channel_stats()"""
    return {
        "handle": handle,
        "viewCount": str(fake.random_int(0, 1_000_000_000)),
        "subscriberCount": str(fake.random_int(0, 1_000_000_000)),
        "videoCount": str(fake.random_int(0, 1000)),
    }
