import requests


class MockResponse:
    """A mock class to simulate 'requests.Response' behavior."""

    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        """Simulate the 'json()' method."""
        return self._json_data

    def raise_for_status(self):
        """Simulate the `raise_for_status()` nethod."""
        if 400 <= self.status_code < 600:
            raise requests.exceptions.HTTPError(f"{self.status_code} Error")
