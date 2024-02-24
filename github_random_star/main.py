import json
import logging as log
import os
import random
import webbrowser
from datetime import datetime
from functools import partial
from pathlib import Path
from threading import Timer
from typing import NamedTuple, Optional
import atexit

import fire  # type: ignore [import-not-found]
import httpx  # type: ignore [import-not-found]

USER_API_URL = "https://api.github.com/users/{user}/starred?page={page}&per_page=30"

if os.name != "nt":
    CACHE_PATH = Path.home() / Path(".cache")
else:
    env = os.getenv("APPDATA")
    if isinstance(env, str):
        CACHE_PATH = Path(env)
    else:
        CACHE_PATH = Path.home()

CACHE_PATH = CACHE_PATH / Path("github_random_star/")


CACHE_PATH.mkdir(parents=True, exist_ok=True)
CACHE_FILE = CACHE_PATH / Path("cache.json")

SELECTION_CACHE = CACHE_PATH / Path("selections.json")

IGNORE_FILE = CACHE_PATH / Path("ignore.json")


class AccountMissingError(TypeError):
    "GitHub account was not provided through flags or an environment variable."


class StarredItem(NamedTuple):
    repo_id: int
    name: str
    url: str


def retrieve_cache(account: str, refresh: bool) -> set[StarredItem]:
    if CACHE_FILE.exists() and not refresh:
        with CACHE_FILE.open("r", encoding="utf-8") as file:
            cache_data = json.load(file)

        log.info(
            "Cache last refreshed on the %s.",
            datetime.fromisoformat(cache_data["date"]).date().isoformat(),
        )
        if cache_data.get("account") == account:
            cache_data = {StarredItem(*item) for item in cache_data["data"]}
            return cache_data

        log.warning("Cache is storing a different account.")

    log.info("Requesting data from Github")

    headers = {"X-GitHub-Api-Version": "2022-11-28"}
    API_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")
    if API_TOKEN is not None:
        log.info("Using provided GitHub API token")
        headers["Authorization"] = f"Bearer {API_TOKEN}"

    data = set()

    page = 1
    while True:
        log.info("Requesting starred items page %s", page)
        formatted_url = USER_API_URL.format(user=account, page=page)
        request = httpx.get(formatted_url, timeout=20, headers=headers)

        if request.status_code != 200:
            raise ConnectionError(
                "Connection failed to get starred items for {account}.\
                Status Code: {request.status_code}"
            )

        response: list = request.json()
        if not response:
            break

        for item in response:
            tp = StarredItem(item["id"], item["full_name"], item["html_url"])
            data.add(tp)

        page += 1

    with CACHE_FILE.open("w", encoding="utf-8") as file:
        container = {
            "account": account,
            "date": datetime.now().isoformat(),
            "data": tuple(data),
        }
        json.dump(container, file)

    return data


def extract_selection(path: Path) -> list[StarredItem]:
    data = []
    if path.exists():
        with path.open("r", encoding="utf-8") as file:
            selections = json.load(file)

        data = [StarredItem(*item) for item in selections]

    return data


def item_selection(
    starred_items: set[StarredItem],
    total: int,
    max_history: int = 100,
    ignore: bool = True,
) -> None:
    selections = extract_selection(SELECTION_CACHE)

    starred_items = starred_items - starred_items.intersection(selections)

    if IGNORE_FILE.exists():
        if ignore:
            ignore_list = extract_selection(IGNORE_FILE)
            starred_items = starred_items - starred_items.intersection(ignore_list)
    else:
        with IGNORE_FILE.open("w", encoding="utf-8") as file:
            json.dump([], file)

    items = random.sample(tuple(starred_items), total)

    print("Which item would you like to select today?")
    while True:
        for i, star in enumerate(items, start=1):
            if not isinstance(star, StarredItem):
                star = StarredItem(*star)

            print(f"{i}. {star.name}")

        try:
            selection = int(input("> "))
            if selection - 1 in range(total):
                break
        except ValueError:
            pass

        print(f"Select an item within the range of 1 and {total}")

    selected_item = StarredItem(*items[selection - 1])

    log.info("Opening %s", selected_item.url)

    t = Timer(1, partial(webbrowser.get().open, selected_item.url))
    atexit.register(t.cancel)
    t.start()

    selections.insert(0, selected_item)
    if len(selections) > max_history:
        selections = selections[: -(len(selections) - max_history)]

    with SELECTION_CACHE.open("w", encoding="utf-8") as file:
        json.dump(selections, file)


def main(
    account: Optional[str] = None,
    total: int = 3,
    refresh: bool = False,
    max_history: int = 100,
    ignore: bool = True,
) -> None:
    log.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=log.INFO,
    )

    if account is None:
        account = os.environ.get("GITHUB_ACCOUNT")
        if account is None:
            raise AccountMissingError()

    starred_items = retrieve_cache(account, refresh)

    log.info("Total amount of starred items: %s", len(starred_items))

    item_selection(starred_items, total, max_history, ignore)

    log.info("Done!")


if __name__ == "__main__":
    fire.Fire(main)
