from random import randint
from datetime import datetime
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
        responses[f"Page_{page}" if page > 0 else None] = {
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
#   YouTube Video Data. Each part has its own function to generate mock data.
##
def mock_request_video_snippet_part():
    """Generate a mock video snippet."""
    return {
        "publishedAt": published_at(),
        "title": fake.sentence(nb_words=3),
        "description": fake.sentence(nb_words=10),
        # Note: thumbnails mocks only the partial thumbnails dictionary: the default url
        "thumbnails": {"default": {"url": fake.image_url()}},
    }


def mock_request_content_details_part():
    """Generate a mock video content details."""
    return {
        "duration": f"PT{randint(1, 60)}M{randint(0, 59)}S",
    }


def mock_request_video_statistics_part():
    """Generate a mock video statistics."""
    return {
        "view_count": str(fake.random_int(0, 1_000_000_000)),
        "like_count": str(fake.random_int(0, 1_000_000)),
        "favorite_count": str(fake.random_int(0, 1_000_000)),
        "comment_count": str(fake.random_int(0, 1_000_000)),
    }


def mock_request_video_data_item(video_id):
    return {
        "kind": "youtube#video",
        "etag": fake.md5(raw_output=False),
        "id": video_id,
        "snippet": mock_request_video_snippet_part(),
        "contentDetails": mock_request_content_details_part(),
        "statistics": mock_request_video_statistics_part(),
    }


def mock_request_video_statistics_item(video_id):
    return {
        "kind": "youtube#video",
        "etag": fake.md5(raw_output=False),
        "id": video_id,
        "statistics": mock_request_video_statistics_part(),
    }


def mock_request_video_api_data(video_ids):
    return {
        "kind": "youtube#videoListResponse",
        "etag": fake.md5(raw_output=False),
        "items": [mock_request_video_data_item(video_id) for video_id in video_ids],
    }


def mock_request_video_api_statistics(video_ids):
    return {
        "kind": "youtube#videoListResponse",
        "etag": fake.md5(raw_output=False),
        "items": [
            mock_request_video_statistics_item(video_id) for video_id in video_ids
        ],
    }


##
#   Mock extracted data. Each API request function will have a corresponding mock function.
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


def mock_video_ids(num_ids=150):
    """Use to mock the output of get_video_ids_from_api()"""
    return [fake.lexify("???????") for id in range(num_ids)]


def mock_video_data(video_id):
    """Use to mock the data part of get_video_data_from_api()"""
    raw_published_at = published_at()

    return {
        "youtube_video_id": video_id,
        "published_at": datetime.strptime(raw_published_at, "%Y-%m-%dT%H:%M:%SZ"),
        "title": fake.sentence(nb_words=3),
        "description": fake.sentence(nb_words=10),
        "thumbnail_url": fake.image_url(),
        "duration": fake.random_int(1, 3600),
    }


def mock_video_stats(video_id):
    """Use to mock the data part of get_video_data_from_api() and to mock get_video_stats_from_api()"""
    return {
        "youtube_video_id": video_id,
        "view_count": fake.random_int(1, 1_000_000_000),
        "like_count": fake.random_int(1, 1_000_000_000),
        "favorite_count": fake.random_int(1, 1_000_000_000),
        "comment_count": fake.random_int(1, 1_000_000_000),
    }


def mock_request_video_data(video_ids):
    """Use to mock the output of get_video_data_from_api()"""
    return [
        (
            mock_video_data(video_id),
            mock_video_stats(video_id),
        )
        for video_id in video_ids
    ]
