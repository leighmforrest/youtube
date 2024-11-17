from pathlib import Path
from test.mocks import MockDownloadResponse

import pytest


@pytest.fixture
def temp_file_path(tmpdir):
    """Fixture to create and clean up a temporary file path."""
    return Path(tmpdir) / "test.txt"


@pytest.fixture
def mock_dbm(monkeypatch):
    mock_db = {}

    class MockDBM:
        def __init__(self):
            pass

        def __enter__(self):
            return mock_db

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    monkeypatch.setattr("dbm.open", lambda *args, **kwargs: MockDBM())

    return mock_db


@pytest.fixture
def mock_download_200(monkeypatch):
    mock_response = MockDownloadResponse(
        content=b"ItemOne,ItemTwo", status_code=200, headers={"ETag": "SomeEtag"}
    )
    monkeypatch.setattr("requests.get", lambda *arg, **kwargs: mock_response)


@pytest.fixture
def mock_download_304(monkeypatch):
    mock_response = MockDownloadResponse(
        content=b"",
        status_code=304,
    )
    monkeypatch.setattr("requests.get", lambda *arg, **kwargs: mock_response)


@pytest.fixture
def mock_download_200(monkeypatch):
    mock_response = MockDownloadResponse(
        content=b"ItemOne,ItemTwo", status_code=200, headers={"etag": "SomeEtag"}
    )
    monkeypatch.setattr("requests.get", lambda *arg, **kwargs: mock_response)
