import argparse
import asyncio
import collections
import os
from typing import Protocol

import httpx

from py_link_detective import __version__
from py_link_detective.detective import (
    ConsolePrinter,
    JsonPrinter,
    get_links,
    get_url_state,
    is_duplicate_checker,
)


def cli_args():
    parser = argparse.ArgumentParser(
        description="A simple implementation of a dead link detection tool using python asyncio library"
    )

    # Add version argument
    parser.add_argument(
        "--version", "-v", action="version", version=f"%(prog)s v{__version__}"
    )

    # number of concurrent request
    parser.add_argument(
        "--num_async_requests",
        "-n",
        type=int,
        default=10,
        metavar="",
        help="number of concurrent request at a time, default is 10",
    )

    parser.add_argument(
        "--timeout",
        "-t",
        type=int,
        default=5,
        metavar="",
        help="timeout for each request, default is 5 seconds",
    )

    # adding a group for printer choice(console / json)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-c",
        action="store_true",
        help="use console for output",
    )
    group.add_argument(
        "-j",
        action="store_true",
        help="use a json file(in the current path) for output",
    )

    # Add URL argument
    parser.add_argument(
        "url",
        metavar="url",
        type=str,
        help="The url of the website to be checked",
    )

    return parser.parse_args()


class Printer(Protocol):
    def print(self, url: str, result: dict[int, list]): ...


async def worker(args: argparse.Namespace, printer: Printer):
    is_duplicate = is_duplicate_checker()
    semaphore = asyncio.Semaphore(args.num_async_requests)
    client = httpx.AsyncClient(timeout=args.timeout)
    results = collections.defaultdict(list)

    tasks = []
    for url in get_links(args.url):
        if is_duplicate(url):
            continue

        task = asyncio.create_task(get_url_state(url, semaphore, client))
        task.add_done_callback(lambda x, url=url: results[x.result()].append(url))  # type: ignore
        tasks.append(task)

    await asyncio.gather(*tasks)

    printer.print(args.url, results)


def main():
    args = cli_args()
    if args.j:
        asyncio.run(worker(args, JsonPrinter("./output.json")))
    else:
        asyncio.run(worker(args, ConsolePrinter()))
