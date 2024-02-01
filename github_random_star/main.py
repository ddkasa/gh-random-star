import json
import logging as log
import os
import random
import webbrowser
from datetime import datetime
from os.path import exists
from pathlib import Path
from typing import NamedTuple, Optional

import fire
import httpx

USER_API_URL = "https://api.github.com/users/{user}/starred?page={page}&per_page=30"

CACHE_PATH = Path("cache")
CACHE_PATH.mkdir(parents=True, exist_ok=True)
CACHE_FILE = CACHE_PATH / Path("cache.json")

SELECTION_CACHE = CACHE_PATH / Path("selections.cache")


class StarredItem(NamedTuple):
    repo_id: int
    name: str
    url: str


def retrieve_cache(account: str, refresh: bool) -> set[StarredItem]:
    if CACHE_FILE.exists() and not refresh:
        with CACHE_FILE.open("r", encoding="utf-8") as file:
            file = json.load(file)

            log.info(
                "Cache last refreshed on the %s.",
                datetime.fromisoformat(file["date"]).date().isoformat(),
            )
            return file["data"]

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
        container = {"date": datetime.now().isoformat(), "data": tuple(data)}
        file.write(json.dumps(container))

    return data


def item_selection(starred_items: set[StarredItem], total: int) -> None:
    # if SELECTION_CACHE.exists():
    #     with SELECTION_CACHE.open("r", encoding="utf-8") as file:
    #         selection_file = json.load(file)

    item = random.sample(tuple(starred_items), total)

    for star in item:
        star = StarredItem(*star)
        print(star)


def main(account: Optional[str] = None, total: int = 3, refresh: bool = False) -> None:
    log.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=log.INFO,
    )

    if account is None:
        account = os.environ.get("GITHUB_ACCOUNT")
        if account is None:
            raise ValueError(
                "Account not provided from arguments or environment variables."
            )

    starred_items = retrieve_cache(account, refresh)

    log.info("Total amount of starred items: %s", len(starred_items))

    item_selection(starred_items, total)


if __name__ == "__main__":
    fire.Fire(main)
