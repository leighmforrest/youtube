import json
from test.data_for_tests import REQUEST_SET
from test.helpers import generate_cache_key
from test.mocks import MockResponse

import pytest
import requests

from youtube.request import (download_file_with_cache, get_with_cache,
                             get_without_cache)


@pytest.mark.parametrize("url,params,etag,data", REQUEST_SET)
def test_cache_miss(capsys, monkeypatch, mock_dbm, url, params, data, etag):
    # make a cached item
    cache_key = generate_cache_key(url, params)
    bogus_data = f"{data}-old"
    data_dict = {"etag": f"{etag}Mi$$", "body": bogus_data}
    mock_dbm[cache_key] = json.dumps(data_dict)

    # mock a 200 response
    mock_response = MockResponse(data, status_code=200, headers={"ETag": etag})
    monkeypatch.setattr("requests.get", lambda url, headers=None: mock_response)

    result = get_with_cache(url, params)
    captured = capsys.readouterr()

    assert result == data
    assert cache_key in mock_dbm
    assert json.dumps(bogus_data) not in mock_dbm[cache_key]
    assert json.dumps(data) in mock_dbm[cache_key]
    assert f"Cache miss: {url}" in captured.out


@pytest.mark.parametrize("url,params,etag,data", REQUEST_SET)
def test_get_with_cache_not_cached(monkeypatch, mock_dbm, url, params, data, etag):
    mock_response = MockResponse(data, status_code=200, headers={"ETag": etag})
    monkeypatch.setattr("requests.get", lambda url, headers=None: mock_response)

    cache_key = generate_cache_key(url, params)
    result = get_with_cache(url, params)

    assert result == data
    assert cache_key in mock_dbm


@pytest.mark.parametrize("url,params,etag,data", REQUEST_SET)
def test_get_with_cache_hit(capsys, monkeypatch, mock_dbm, url, params, data, etag):
    cache_key = generate_cache_key(url, params)
    data_dict = {"etag": etag, "body": data}
    mock_dbm[cache_key] = json.dumps(data_dict)

    # Mock a 304 response
    mock_response = MockResponse("", status_code=304)
    monkeypatch.setattr("requests.get", lambda url, headers=None: mock_response)

    result = get_with_cache(url, params)
    captured = capsys.readouterr()

    assert result == data
    assert cache_key in mock_dbm
    assert json.dumps(data_dict) in mock_dbm[cache_key]
    assert f"Cache hit: {url}" in captured.out


@pytest.mark.parametrize("url,params,etag,data", REQUEST_SET)
def test_get_with_cache_not_found_404_cached(
    monkeypatch, mock_dbm, url, params, data, etag
):
    cache_key = generate_cache_key(url, params)
    data_dict = {"etag": etag, "body": data}
    mock_dbm[cache_key] = json.dumps(data_dict)

    # Mock a 304 response
    mock_response = MockResponse("", status_code=404)
    monkeypatch.setattr("requests.get", lambda url, headers=None: mock_response)

    with pytest.raises(requests.exceptions.HTTPError):
        get_with_cache(url, params)


@pytest.mark.parametrize("url,params,etag,data", REQUEST_SET)
def test_get_with_cache_not_found_404_not_cached(
    monkeypatch, mock_dbm, url, params, data, etag
):
    # Mock a 304 response
    mock_response = MockResponse("", status_code=404)
    monkeypatch.setattr("requests.get", lambda url, headers=None: mock_response)

    with pytest.raises(requests.exceptions.HTTPError):
        get_with_cache(url, params)


def test_cached_response_304(mock_download_304, temp_file_path, mock_dbm):
    params = {"id": 1}
    url = "http://www.example.com/example.txt"
    cache_key = generate_cache_key(url, params)

    # Manually add the cached respose to the mock_dbm
    mock_dbm[cache_key] = json.dumps(
        {"etag": "SomeEtag", "file_path": str(temp_file_path)}
    )

    temp_file_path.write_bytes(b"ItemOne,ItemTwo")
    file_path = download_file_with_cache(url, temp_file_path, params)

    with open(file_path, "rb") as f:
        assert f.read() == b"ItemOne,ItemTwo"

    assert cache_key in mock_dbm


def test_cached_response_200(mock_download_200, temp_file_path, mock_dbm):
    params = {"id": 1}
    url = "http://www.example.com/example.txt"
    cache_key = generate_cache_key(url, params)

    file_path = download_file_with_cache(url, temp_file_path, params)

    with open(file_path, "rb") as f:
        assert f.read() == b"ItemOne,ItemTwo"

    assert cache_key in mock_dbm


def test_cached_response_invalid_json_error(
    mock_download_200, capsys, temp_file_path, mock_dbm
):
    params = {"id": 1}
    url = "http://www.example.com/example.txt"
    cache_key = generate_cache_key(url, params)

    # Manually add the cached respose to the mock_dbm
    mock_dbm[cache_key] = b"SomeInvalidItem"

    temp_file_path.write_bytes(b"ItemOne,ItemTwo")
    file_path = download_file_with_cache(url, temp_file_path, params)

    with open(file_path, "rb") as f:
        assert f.read() == b"ItemOne,ItemTwo"

    assert cache_key in mock_dbm

    captured = capsys.readouterr()
    assert "Warning: Cached data is not valid JSON." in captured.out


@pytest.mark.parametrize("url,params,etag,data", REQUEST_SET)
def test_get_without_cache_200(monkeypatch, mock_dbm, url, params, data, etag):
    mock_response = MockResponse(data, status_code=200, headers={"ETag": etag})
    monkeypatch.setattr("requests.get", lambda url, headers=None: mock_response)

    result = get_without_cache(url, params)
    assert result == data
