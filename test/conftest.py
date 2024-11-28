import pytest
import requests

from test.mocks import MockResponse


@pytest.fixture
def mock_response(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse(json_data={"message": "response"})
    
    monkeypatch.setattr(requests, "get", mock_get)