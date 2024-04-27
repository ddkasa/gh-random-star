import json
import logging
from datetime import datetime
from pathlib import Path
from typing import NamedTuple, Optional

import httpx

from github_random_star.version import __version__

log = logging.getLogger("GitHub Random Star")


class StarredItem(NamedTuple):
    repo_id: int
    name: str
    url: str


class GithubAPI:
    USER_API_URL = "https://api.github.com/users/{user}/starred?page={page}&per_page=30"

    def __init__(
        self,
        account: str,
        cache_location: Path,
        *,
        refresh: bool = False,
        max_results: Optional[int] = None,
        token: Optional[str] = None,
    ) -> None:
        self.account = account
        self.headers = self.create_headers(token)
        self.cache_path = cache_location
        self.refresh = refresh
        self.max_results = max_results

    def create_headers(self, token: Optional[str] = None) -> None:
        headers = {"X-GitHub-Api-Version": "2022-11-28"}

        if token:
            log.info("Using provided GitHub API token")
            headers["Authorization"] = f"Bearer {token}"
        else:
            log.warning(
                "No GitHub API token provided. Using public access with a lower rate limit."
            )

        return headers

    def collect_starred_items(self) -> set[StarredItem]:
        cache = self.load_cached_items()
        if cache:
            return cache

        log.info("Requesting data from Github")

        data = set()

        page = 1
        while True:
            response = self.get_starred_items(page)

            if not response:
                break

            for item in response:
                tp = StarredItem(
                    item["id"],
                    item["full_name"],
                    item["html_url"],
                )
                data.add(tp)
                if self.max_results and len(data) >= self.max_results:
                    break

            if self.max_results and len(data) >= self.max_results:
                break

            page += 1

        self.save_cached_items(data)

        return data

    def get_starred_items(self, page: int = 1) -> list[dict]:
        log.info("Requesting starred items page %s", page)
        url = self.USER_API_URL.format(user=self.account, page=page)
        response = httpx.get(url, headers=self.headers)
        response.raise_for_status()

        if response.status_code != 200:
            err = "Connection failed to get starred items for %s. \
                Status Code: %s"
            log.error(err, self.account, response.status_code)
            raise ConnectionError(err % self.account, response.status_code)

        return response.json()

    def load_cached_items(self) -> set[StarredItem] | None:
        cache_path = self.cache_path / Path("cache.json")

        if cache_path.exists() and not self.refresh:
            with cache_path.open("r", encoding="utf-8") as file:
                cache_data = json.load(file)

            log.info(
                "Cache last refreshed on the %s.",
                datetime.fromisoformat(cache_data["date"]).date().isoformat(),
            )
            version = cache_data.get("version")


            account = cache_data.get("account")
            if account == self.account:
                cache_data = {StarredItem(*item) for item in cache_data["data"]}
                if version != __version__:
                    log.warning(
                        "Cache is from a different version. Current: %s - Stored: %s",
                        __version__,
                        version,
                    )
                    self.save_cached_items(cache_data)
                return cache_data

            if account != self.account:
                log.warning("Cache is storing a different account.")

        return None

    def save_cached_items(self, data: set[StarredItem]) -> None:
        cache_path = self.cache_path / Path("cache.json")
        with cache_path.open("w", encoding="utf-8") as file:
            container = {
                "version": __version__,
                "account": self.account,
                "date": datetime.now().isoformat(),
                "data": tuple(data),
            }
            json.dump(container, file)
