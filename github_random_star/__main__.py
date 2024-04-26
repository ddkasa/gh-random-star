import json
import logging
import os
import random
import subprocess
from pathlib import Path
from typing import Optional

import fire

from github_random_star.api import GithubAPI, StarredItem

log = logging.getLogger("GitHub Random Star")


class AccountMissingError(TypeError):
    "GitHub account was not provided through flags or an environment variable."


def extract_selection(path: Path) -> list[StarredItem]:
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

        data = [StarredItem(*item) for item in selections]

    return data


def item_selection(
    starred_items: set[StarredItem],
    cache_path: Path,
    *,
    total: int,
    max_history: int = 100,
    ignore: bool = True,
) -> None:
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
    selection_cache = cache_path / Path("selections.json")
    ignore_file = cache_path / Path("ignore.json")

    og_len = len(starred_items)

    selections = extract_selection(selection_cache)
    if max_history != -1:
        starred_items = starred_items - starred_items.intersection(selections)

    if ignore_file.exists():
        ignore_list = extract_selection(ignore_file)
        if ignore:
            starred_items = starred_items - starred_items.intersection(ignore_list)
    else:
        ignore_list = []
        with ignore_file.open("w", encoding="utf-8") as file:
            json.dump(ignore_list, file)

    items = random.sample(tuple(starred_items), total)

    print("Which item would you like to select today?")
    print("Note: Add .1 to number to add to ignore list")
    while True:
        for i, star in enumerate(items, start=1):
            if not isinstance(star, StarredItem):
                star = StarredItem(*star)

            print(f"{i}. {star.name}")

        try:
            selection = float(input("> "))
            if int(selection - 1) in range(total):
                break
        except ValueError:
            pass

        print(f"Select an item within the range of 1 and {total}")

    # TODO: Add a way of directly adding items to ignore list.
    selected_item = StarredItem(*items[int(selection - 1)])

    log.info("Opening %s", selected_item.url)

    subprocess.run(
        ["python", "-m", "webbrowser", "-t", selected_item.url],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if selection % 1 != 0.1:
        log.info("Adding %s to ignore list", selected_item.name)
        ignore_list.append(selected_item)
        with ignore_file.open("w", encoding="utf-8") as file:
            json.dump(ignore_list, file)

    selections.insert(0, selected_item)
    if len(selections) > max_history and max_history > 0:
        selections = selections[: -(len(selections) - max_history)]

    if og_len == len(starred_items) and max_history == -1:
        selections = []

    with selection_cache.open("w", encoding="utf-8") as file:
        json.dump(selections, file)


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

    token = os.environ.get("GH_STAR_TOKEN")
    github_api = GithubAPI(
        account,
        cache_path,
        refresh=refresh,
        max_results=max_results,
        token=token,
    )

    starred_items = github_api.collect_starred_items()

    log.info("Total amount of starred items: %s", len(starred_items))

    item_selection(
        starred_items,
        cache_path,
        total=total,
        max_history=max_history,
        ignore=ignore,
    )

    log.info("Done!")


if __name__ == "__main__":
    fire.Fire(main)
