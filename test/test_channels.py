import requests

from youtube.channels import (
    get_channel,
    get_channel_data_from_api,
    get_channel_stats,
    get_channel_stats_from_api,
)
from youtube.db.models import Channel


def test_channels(youtube_channel, youtube_channel_statistics):
    assert (
        youtube_channel["items"][0]["id"]
        == youtube_channel_statistics["items"][0]["id"]
    )


def test_get_channel_from_api(monkeypatch, youtube_channel, test_handle):

    def mock_request_get(url, params):
        # Simulate an appropriate response for the given URL and params
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(youtube_channel, 200)

    monkeypatch.setattr(requests, "get", mock_request_get)

    api_data = get_channel_data_from_api(test_handle)

    youtube_channel = youtube_channel["items"][0]
    expected_data = {
        "handle": test_handle,
        "youtube_channel_id": youtube_channel["id"],
        "title": youtube_channel["snippet"]["title"],
        "description": youtube_channel["snippet"]["description"],
        "thumbnail_url": youtube_channel["snippet"]["thumbnails"]["default"]["url"],
        "upload_playlist": youtube_channel["contentDetails"]["relatedPlaylists"][
            "uploads"
        ],
    }
    assert api_data == expected_data


def test_get_channel_stats_from_api(
    monkeypatch, youtube_channel_statistics, db_channel
):

    def mock_request_get(url, params):
        # Simulate an appropriate response for the given URL and params
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(youtube_channel_statistics, 200)

    monkeypatch.setattr(requests, "get", mock_request_get)

    api_data = get_channel_stats_from_api(db_channel)

    statistics = youtube_channel_statistics["items"][0]["statistics"]

    id = db_channel.id
    expected_data = {
        "channel_id": id,
        "subscriber_count": int(statistics["subscriberCount"]),
        "video_count": int(statistics["videoCount"]),
        "view_count": int(statistics["viewCount"]),
    }
    assert api_data == expected_data


def test_get_channel_stats(
    monkeypatch, youtube_channel_statistics, db_channel, session, test_handle
):

    def mock_request_get(url, params):
        # Simulate an appropriate response for the given URL and params
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(youtube_channel_statistics, 200)

    monkeypatch.setattr(requests, "get", mock_request_get)

    returned_data = get_channel_stats(session, db_channel)

    statistics = youtube_channel_statistics["items"][0]["statistics"]
    id = db_channel.id

    expected_data = {
        "channel_id": id,
        "subscriber_count": int(statistics["subscriberCount"]),
        "video_count": int(statistics["videoCount"]),
        "view_count": int(statistics["viewCount"]),
    }

    assert returned_data.channel_id == expected_data["channel_id"]
    assert returned_data.subscriber_count == expected_data["subscriber_count"]
    assert returned_data.video_count == expected_data["video_count"]
    assert returned_data.view_count == expected_data["view_count"]


def test_get_channel_stats_existing_fresh(session, db_channel_stats, db_channel):
    results = get_channel_stats(session, db_channel)
    assert results == db_channel_stats


def test_get_channel_existing_channel(session, test_handle, db_channel):
    results = get_channel(session, test_handle)
    assert results == db_channel


def test_get_channel_new_channel(session, test_handle, monkeypatch, youtube_channel):
    def mock_request_get(url, params):
        # Simulate an appropriate response for the given URL and params
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(youtube_channel, 200)

    monkeypatch.setattr(requests, "get", mock_request_get)
    results = get_channel(session, test_handle)
    db_data = Channel.get_by_handle(session, test_handle)
    assert results == db_data
