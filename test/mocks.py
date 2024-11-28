class MockResponse:
    def __init__(self, json_data=None, text_data=None, status_code=200):
        self.json_data = json_data
        self.text_data = text_data
        self.status_code = status_code
    
    def json(self):
        if self.json_data is not None:
            return self.json_data
        raise ValueError("No JSON data available")
    
    @property
    def test(self):
        if self.text_data is not None:
            return self.text_data
        raise ValueError("No text data available")