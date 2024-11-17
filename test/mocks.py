import requests


class MockResponse(object):
    def __init__(self, content, status_code, headers=None):
        self.content = content
        self.status_code = status_code
        self.headers = headers or {}

    @property
    def text(self):
        return str(self.content)

    def raise_for_status(self):
        if self.status_code != 200 or self.status_code != 304:
            raise requests.exceptions.HTTPError()


class MockDownloadResponse(object):
    """Class for mocking a requests.get call that downloads a file."""

    def __init__(self, content, status_code=200, headers=None):
        self.content = content
        self.status_code = status_code
        self.headers = headers
        self.iter_content_called = False

    def iter_content(self, chunk_size=1024):
        self.iter_content_called = True
        return [
            self.content[i : i + chunk_size]
            for i in range(0, len(self.content), chunk_size)
        ]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def raise_for_status(self):
        pass
