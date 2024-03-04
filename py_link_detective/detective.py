import asyncio
import json
from typing import Callable
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup


def get_links(url: str):
    try:
        response = httpx.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all("a"):
            href = link.get("href")
            yield urljoin(url, href)

    except httpx.HTTPError as e:
        print(f"An error occurred while fetching {url}, details: {repr(e)}")


def is_duplicate_checker() -> Callable[[str], bool]:
    url_store: dict[str, bool] = {}

    def is_duplicate(url: str) -> bool:
        is_seen = url_store.get(url, False)
        if not is_seen:
            url_store[url] = True

        return is_seen

    return is_duplicate


def retry_on_error(retries: int = 3, delay: float = 1.0):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for i in range(retries):
                status = await func(*args, **kwargs)
                if status not in [0, -1]:
                    return status

                await asyncio.sleep(delay * (i + 1))  # Introduce delay between retries
            return -1  # Return -1 if all retries fail

        return wrapper

    return decorator


@retry_on_error()
async def get_url_state(
    url: str, semaphore: asyncio.Semaphore, client: httpx.AsyncClient
) -> int:
    async with semaphore:
        try:
            response = await client.get(url)
            return response.status_code

        except httpx.HTTPError as err:
            print(f"error fetching {url}, details: {repr(err)}")
            return 0

        except Exception as err:
            print(f"unknown error fetching {url}, details: {repr(err)}")
            return -1


class ConsolePrinter:
    def print(self, url, result: dict[int, list]):
        print(
            f"\n################################# {url} #################################\n"
        )

        for code, urls in result.items():
            for url in urls:
                print("{:>3} | {:<40} ".format(code, url))

        print("-------------------------------------------")


class JsonPrinter:
    def __init__(self, path) -> None:
        self.file_path = path

    def print(self, url, result: dict[int, list]):

        with open(self.file_path, "w") as json_file:
            json.dump(result, json_file, indent=4)

        print(f"JSON output has been written to {self.file_path}")
