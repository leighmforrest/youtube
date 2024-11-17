import dbm
import hashlib
import json
import os
from pathlib import Path

import requests

get_cache_key = lambda full_url: hashlib.sha256(full_url.encode("utf-8")).hexdigest()


def get_full_url(url, params=None):
    """Get a URL with the params as query strings."""
    req = requests.PreparedRequest()
    req.prepare_url(url, params)
    return req.url


def add_to_cache(response, cache_db, cache_key):
    body = response.text
    etag = response.headers.get("ETag")
    data_dict = {"etag": etag, "body": body}
    cache_db[cache_key] = json.dumps(data_dict)

    return data_dict


def download_file(full_url, file_path, **kwargs):
    """Download a file directly. Return response for further
    file processing."""
    print("Downloading file...")
    response = requests.get(full_url, stream=True, **kwargs)
    response.raise_for_status()

    # Write the contents to the file
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=10 * 1024):
            file.write(chunk)

    return response


def get_without_cache(url, params=None, headers={}):
    """Retrieve data without any caching."""
    full_url = get_full_url(url, params)
    response = requests.get(full_url, headers=headers)
    print(f"Fetching data from URL {url}")
    return response.text


def get_with_cache(url, params=None, headers={}):
    full_url = get_full_url(url, params)
    cache_key = get_cache_key(full_url)

    with dbm.open("cache", "c") as cache_db:
        if cache_key in cache_db:
            cached_data = json.loads(cache_db[cache_key])
            cached_etag = cached_data.get("etag")
            cached_body = cached_data.get("body")

            headers = headers if isinstance(headers, dict) else {}
            headers = {**headers, "If-None-Match": cached_etag}

            response = requests.get(full_url, headers=headers)

            if response.status_code == 304:
                print(f"Cache hit: {full_url} retrieving cache")
                return cached_body

            elif response.status_code == 200:
                print(f"Cache miss: {full_url} retrieving data")
                data_dict = add_to_cache(response, cache_db, cache_key)
                return data_dict["body"]
            else:
                response.raise_for_status()
        else:
            print(f"Cache miss: {full_url} retrieving new data")
            response = requests.get(full_url)

            # Must be 200 for data storage
            if response.status_code != 200:
                response.raise_for_status()

            data_dict = add_to_cache(response, cache_db, cache_key)

            return data_dict["body"]


def download_file_with_cache(url, file_path, params=None, **kwargs):
    # Create the directory for the file if it doesn't exist
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path_string = str(file_path)

    # Create the cache key
    full_url = get_full_url(url, params)
    cache_key = get_cache_key(full_url)

    with dbm.open("cache", "c") as cache:
        cached_data = cache.get(cache_key)

        if cached_data:
            try:
                cached_data = json.loads(cached_data)
                cached_etag = cached_data.get("etag")
                cached_file_path = cached_data.get("file_path")

                if os.path.exists(cached_file_path):
                    headers = {"If-None-Match": cached_etag}
                    response = requests.get(full_url, headers=headers)
                    if response.status_code == 304:
                        print("Cache hit: File not modified, using cached file")
                        return cached_file_path
            except json.JSONDecodeError:
                print("Warning: Cached data is not valid JSON.")

        response = download_file(full_url, file_path, **kwargs)

        # Update the cache with the new file info
        cache[cache_key] = json.dumps(
            {"etag": response.headers.get("ETag"), "file_path": file_path_string}
        )

        print("File downloaded and cached.")

        return file_path_string
