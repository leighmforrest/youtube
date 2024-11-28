class MockResponse:
    def __init__(self, json_data=None, text_data=None, status_code=200, params=None):
        self.json_data = json_data
        self.text_data = text_data
        self.status_code = status_code
        self.params = params or {}  # Default to an empty dictionary if no params are provided
    
    def json(self):
        if self.json_data is not None:
            return self.json_data
        raise ValueError("No JSON data available")
    
    @property
    def text(self):
        if self.text_data is not None:
            return self.text_data
        raise ValueError("No text data available")
