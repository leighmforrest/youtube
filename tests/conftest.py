import pytest
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from tests.mocks import MockResponse
from tests.data import (
    mock_channels_list_api_data,
    mock_channels_list_api_stats,
    mock_request_playlist_items_api_paginated_dictionary,
    mock_video_ids,
    mock_request_video_api_data,
    mock_request_video_api_statistics,
    db_mock_channel,
    db_mock_video,
    db_mock_video_stats,
    db_mock_channel_stats,
)
from youtube.db import init_db
from youtube.db.models import Channel, Video, VideoStats, ChannelStats


@pytest.fixture
def test_handle():
    return "@YourTubeChannel"


@pytest.fixture
def mock_response(monkeypatch):
    def _mock_response(json_data, status_code=200):
        def mock_requests_get(*args, **kwargs):
            return MockResponse(json_data=json_data, status_code=status_code)

        monkeypatch.setattr("requests.get", mock_requests_get)

    return _mock_response


@pytest.fixture
def mock_channel_list_api_data_request(mocker):
    test_response_data = mock_channels_list_api_data(test_handle)
    mock_get_youtube_request = mocker.patch(
        "youtube.channels.get_youtube_request",
        return_value=test_response_data,
    )

    return mock_get_youtube_request


@pytest.fixture
def mock_channel_list_api_stats_request(mocker):
    test_response_data = mock_channels_list_api_stats(test_handle)
    mock_get_youtube_request = mocker.patch(
        "youtube.channels.get_youtube_request",
        return_value=test_response_data,
    )

    return mock_get_youtube_request


@pytest.fixture
def mock_youtube_playlist_items_pages():
    return mock_request_playlist_items_api_paginated_dictionary()


@pytest.fixture
def mock_youtube_playlist_items_api_request(mock_youtube_playlist_items_pages, mocker):
    def mock_request(endpoint, params):
        page_token = params.get("pageToken", None)
        if page_token in mock_youtube_playlist_items_pages:
            return mock_youtube_playlist_items_pages[page_token]
        else:
            raise ValueError(f"Invalid pageToken: {page_token}")

    mock = mocker.patch("youtube.videos.get_youtube_request", side_effect=mock_request)

    return mock


@pytest.fixture
def mock_youtube_video_ids():
    return mock_video_ids()


@pytest.fixture
def mock_youtube_video_api_request(mock_youtube_video_ids, mocker):
    def mock_request(endpoint, params):
        ids = params.get("id")
        # The id parameter is a comma-separated list of video ids, so split them
        video_ids = ids.split(",") if ids else []
        return mock_request_video_api_data(video_ids)

    mock = mocker.patch("youtube.videos.get_youtube_request", side_effect=mock_request)

    return mock


@pytest.fixture
def mock_youtube_video_statistics_api_request(mock_youtube_video_ids, mocker):
    def mock_request(endpoint, params):
        ids = params.get("id")
        # The id parameter is a comma-separated list of video ids, so split them
        video_ids = ids.split(",") if ids else []
        return mock_request_video_api_statistics(video_ids)

    mock = mocker.patch("youtube.videos.get_youtube_request", side_effect=mock_request)

    return mock


##
#   Database Fixtures
##
@pytest.fixture(scope="function")
def test_session():
    engine, test_session = init_db("sqlite+pysqlite:///:memory:")

    yield test_session

    test_session.close()
    engine.dispose()


@pytest.fixture(scope="function")
def test_channel(test_handle: str, test_session: Session):
    channel_data = db_mock_channel(test_handle)
    channel = Channel(**channel_data)
    test_session.add(channel)
    test_session.commit()

    yield channel


@pytest.fixture(scope="function")
def test_channel_stats(test_channel: Channel, test_session: Session):
    channel_stats_data = db_mock_channel_stats()
    channel_stats = ChannelStats(**channel_stats_data, channel=test_channel)
    test_session.add(channel_stats)
    test_session.commit()

    yield channel_stats


@pytest.fixture(scope="function")
def test_five_videos(test_channel, test_session):
    video_data = [db_mock_video() for _ in range(5)]
    test_videos = [
        Video(**video_dict, channel=test_channel) for video_dict in video_data
    ]
    test_session.add_all(test_videos)
    test_session.commit()

    yield test_videos


@pytest.fixture(scope="function")
def test_seven_videos_with_old_stats(test_channel, test_session):
    video_data = [db_mock_video() for _ in range(7)]
    test_videos = [
        Video(**video_dict, channel=test_channel) for video_dict in video_data
    ]
    test_session.add_all(test_videos)
    test_session.commit()

    yield test_videos


@pytest.fixture(scope="function")
def test_five_videos_stats_current(test_five_videos, test_session):
    video_stats_data_list = [
        {**db_mock_video_stats(), "video": video} for video in test_five_videos
    ]
    video_stats = [VideoStats(**data) for data in video_stats_data_list]
    test_session.add_all(video_stats)
    test_session.commit()

    yield video_stats


@pytest.fixture
def test_seven_videos_stats_old(test_session, test_seven_videos_with_old_stats):
    old_date = datetime.now(tz=timezone.utc) - timedelta(hours=24, minutes=10)

    video_stats_data_list = [
        {**db_mock_video_stats(), "video": video, "created_at": old_date}
        for video in test_five_videos
    ]
    video_stats = [VideoStats(**data) for data in video_stats_data_list]
    test_session.add_all(video_stats)
    test_session.commit()

    yield video_stats
