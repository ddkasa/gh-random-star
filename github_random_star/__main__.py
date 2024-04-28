import json
import logging
import os
import random
import subprocess
from pathlib import Path
from typing import Optional

import fire

from github_random_star.api import GithubAPI

log = logging.getLogger("GitHub Random Star")


class AccountMissingError(TypeError):
    "GitHub account was not provided through flags or an environment variable."


def extract_selection(path: Path) -> list[str]:
    """Extracts selections from a JSON file.

    Args:
        path: Path to the JSON file.

    Returns:
        list(StarredItem): List of starred items from the JSON file. Needs to
            stay a list in order to preserve order when keeping history.
    """

    data = []
    if path.exists():
        with path.open("r", encoding="utf-8") as file:
            selections = json.load(file)
            if "data" in selections:
                selections = selections["data"]

    return data


def user_selection(
    starred_items: set[str],
    total: int,
) -> tuple[str, float]:
    """Selection function where the user chooses a random starred item.

    Args:
        starred_items: Set of starred items from GitHub.
        total: Number of items to select from.

    Returns:
        tuple(StarredItem, float): Selected item and the selection number for
            further processing

    """
    items = random.sample(tuple(starred_items), total)

    print("Which item would you like to select today?")
    print("Note: Add .1 to number to add to ignore list")
    # TODO: Add a way of removing a starred item from a user if api key is present.
    while True:
        for i, star in enumerate(items, start=1):
            print(f"{i}. {star}")

        try:
            selection = float(input("> "))
            if int(selection - 1) in range(total):
                break
        except ValueError:
            pass

        print(f"Select an item within the range of 1 and {total}")

    selected_item = items[int(selection - 1)]

    return selected_item, selection


def item_selection(
    data: dict,
    cache_path: Path,
    *,
    total: int,
    max_history: int = 100,
    ignore: bool = True,
) -> dict:
    """Selection function where the user chooses a random starred item.

    Args:
        starred_items: Set of starred items from GitHub.
        cache_path: Path to the cache directory.
        total: Total of choices the user can pick from.
        max_history: Maximum amount of items to keep in history.
            Defaults to 100. Set to 0 to disable history or -1 to keep all.
        ignore: Whether or not to ignore previously selected items.
            Defaults to True.
    """

    starred_items = set(data["data"])

    # TODO: Need a way of avoiding keeping enough items in the history.
    if max_history != -1:
        starred_items -= starred_items.intersection(set(data["history"]))

    if ignore:
        starred_items -= starred_items.intersection(set(data["ignore"]))

    selected_item, selection = user_selection(starred_items, total)

    gh_url = "https://github.com/" + selected_item

    log.info("Opening %s", gh_url)
    subprocess.run(
        ["python", "-m", "webbrowser", "-t", gh_url],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if round(selection % 1, 1) == 0.1:
        log.info("Adding %s to ignore list", selected_item)
        data["ignore"].append(selected_item)

    data["history"].insert(0, selected_item)
    if len(data["history"]) > max_history and max_history > 0:
        data["history"] = data["history"][: -(len(data["history"]) - max_history)]

    return data


def generate_cache_directory():
    """Setup for cache directory depending on the OS.

    Returns:
        Path: Path to the cache directory.
    """
    if os.getenv("PYTEST_TESTING"):
        CACHE_PATH = Path("tests/files")

    elif os.name != "nt":
        CACHE_PATH = Path.home() / Path(".cache")
    else:
        env = os.getenv("APPDATA")
        if isinstance(env, str):
            CACHE_PATH = Path(env)
        else:
            CACHE_PATH = Path.home()

    CACHE_PATH = CACHE_PATH / Path("github_random_star/")
    CACHE_PATH.mkdir(parents=True, exist_ok=True)

    return CACHE_PATH


def main(
    account: Optional[str] = None,
    total: int = 3,
    refresh: bool = False,
    max_history: Optional[int] = None,
    ignore: bool = True,
    max_results: Optional[int] = None,
) -> None:
    """Basic entrypoint for the CLI script.

    Raises:
        AccountMissingError: If the GitHub account was not provided through
            flags or an environment variables.
    """
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    cache_path = generate_cache_directory()

    if account is None:
        account = os.environ.get("GH_STAR_ACCOUNT")
        if account is None:
            raise AccountMissingError()

    if max_history is None:
        max_history = int(os.environ.get("GH_STAR_MAX_HISTORY", 100))

    token = os.environ.get("GITHUB_ACCESS_TOKEN")
    github_api = GithubAPI(
        account,
        cache_path,
        refresh=refresh,
        max_results=max_results,
        token=token,
    )

    starred_items = github_api.collect_starred_items()

    log.info("Total amount of starred items: %s", len(starred_items))

    data = item_selection(
        starred_items,
        cache_path,
        total=total,
        max_history=max_history,
        ignore=ignore,
    )

    github_api.save_cached_items(data["data"], data)

    log.info("Done!")


if __name__ == "__main__":
    fire.Fire(main)
