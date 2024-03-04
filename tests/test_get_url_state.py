import asyncio

import httpx
import pytest

from py_link_detective.detective import get_url_state


@pytest.fixture
def async_client_mock():
    async_client_mock = AsyncClientMock()
    return async_client_mock


class AsyncClientMock:
    async def get(self, url):
        return self.Response()

    async def raise_unknown_exception(self, url):
        raise Exception("Simulated exception")

    async def raise_httpx_exception(self, url):
        raise httpx.HTTPError("httpxError exception")

    class Response:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_value, traceback):
            pass

        status_code = 200  # Default status code for successful response


@pytest.mark.asyncio
async def test_get_url_state(async_client_mock):
    semaphore = asyncio.Semaphore(5)  # Example semaphore limit

    # Test for a valid URL
    url = "https://www.example.com"
    status_code = await get_url_state(url, semaphore, async_client_mock)
    assert status_code == 200  # Assuming a successful response

    # Test for a non-existent URL
    async_client_mock.Response.status_code = 404
    non_existent_url = "https://www.nonexistentwebsite.com"
    status_code = await get_url_state(non_existent_url, semaphore, async_client_mock)
    assert status_code == 404  # Assuming a not found response

    # Test for a URL that causes an HTTP error
    async_client_mock.get = (
        async_client_mock.raise_httpx_exception
    )  # Simulate HTTP error
    invalid_url = "https://www.invalidwebsite.com"
    status_code = await get_url_state(invalid_url, semaphore, async_client_mock)
    assert status_code == 0  # Assuming an error occurred

    # Test for a URL that causes an unknown error
    async_client_mock.get = async_client_mock.raise_unknown_exception
    unknown_error_url = "https://www.unknownerrorwebsite.com"
    status_code = await get_url_state(unknown_error_url, semaphore, async_client_mock)
    assert status_code == -1  # Assuming an unknown error occurred
