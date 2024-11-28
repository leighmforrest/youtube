import requests

def test_api_call(mock_response):
    response = requests.get("https://www.example.com/api", params={"id": 1})
    assert response.status_code == 200
    assert response.json() == {"message": "response"}
