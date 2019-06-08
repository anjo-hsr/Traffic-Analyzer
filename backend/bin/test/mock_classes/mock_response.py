class MockResponse():
    def __init__(self, status_code=200, content=""):
        self.status_code = status_code
        self.content = content.encode("utf-8")
