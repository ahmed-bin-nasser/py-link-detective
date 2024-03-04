import httpx
import pytest

from py_link_detective.detective import get_links


class MockResponse:
    def __init__(self, text):
        self.text = text


@pytest.fixture
def mock_httpx_get(monkeypatch):
    # Define a mock implementation of httpx.get
    def mock_get(url):
        return MockResponse('<a href="https://example.com"></a>')

    # Replace httpx.get with the mock implementation
    monkeypatch.setattr(httpx, "get", mock_get)


def test_get_links(mock_httpx_get):
    # Test the function with a mock response
    url = "https://www.example.com"
    links = list(get_links(url))

    # Assert the links
    assert len(links) == 1
    assert links[0] == "https://example.com"
