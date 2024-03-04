import argparse
from py_link_detective import __version__


def cli_args():
    parser = argparse.ArgumentParser(
        description="Detective: A simple link checker for websites"
    )

    # Add version argument
    parser.add_argument(
        "--version", "-v", action="version", version=f"%(prog)s v{__version__}"
    )

    # Add URL argument
    parser.add_argument(
        "url",
        metavar="url",
        type=str,
        help="The url of the website to be checked",
    )

    return parser.parse_args()


def main():
    args = cli_args()

    print(args.url)
