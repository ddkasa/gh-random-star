import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import httpx

from github_random_star.version import __version__, process_version

log = logging.getLogger("GitHub Random Star")


class GithubAPI:
    """API wrapper for the GitHub API.

    Handles fetching starred items from the GitHub API and cache.

    Methods:
        create_headers: Creates the headers for the API request.
        collect_starred_items: Main method that run the the class.
        get_starred_items: Fetches starred items from the API.
        load_cached_items: Loads cached items from the cache.
        save_cached_items: Formats saves cached items to a json file.

    Attributes:
        USER_API_URL: URL endpoint template for the API request.
        account: GitHub account name.
        headers: Headers for the API request.
        cache_path: Path to the cache folder.
        refresh: Whether to refresh the cache.
        max_results: Maximum number of starred items to return.
    """

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
        self.version = process_version(__version__)

        self.convert_cache()

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

    def collect_starred_items(self) -> dict[str, Any]:
        """Main method that runs the the class functionality.

        If the cache is valid, it will load it. Otherwise, it will request
        the data from the API and keep requesting until a page is not found or
        the maximum number of results is reached.

        Returns:
            dict: A dictionary with all the data needed to run the main script.
        """
        cache = self.load_cached_items()
        if cache and not self.refresh:
            return cache

        log.info("Requesting data from Github")

        data = set()

        page = 1
        while True:
            response = self.get_starred_items(page)
            if not response:
                break

            for item in response:
                data.add(item["full_name"])
                if self.max_results and len(data) >= self.max_results:
                    break

            if self.max_results and len(data) >= self.max_results:
                break

            page += 1

        return self.save_cached_items(data, cache)

    def get_starred_items(self, page: int = 1) -> list[dict]:
        # REFACTOR: Possibly adjust to use a persistent client instead.
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

    def load_cached_items(self) -> set[str] | None:
        cache_path = self.cache_path / Path(f"{self.account}_cache.json")
        if not cache_path.exists():
            return None

        with cache_path.open("r", encoding="utf-8") as file:
            cache_data = json.load(file)

        log.info(
            "Cache last refreshed on the %s.",
            datetime.fromisoformat(cache_data["date"]).date().isoformat(),
        )

        version = process_version(cache_data.get("version", "0.0.0"))
        if self.version != version:
            log.warning(
                "Cache is from a different version. Current: %s - Stored: %s",
                __version__,
                version,
            )

        return self.save_cached_items(cache_data.get("data", []), cache_data)

    def save_cached_items(
        self,
        data: set[str],
        container: Optional[dict] = None,
    ) -> dict[str, Any]:
        """Formats saves cached items to a json file.

        Is meant to be used as a function to return starred data.

        Args:
            data: A set of starred items.
            container: A dictionary with all the data needed to run the main
                script.
        Returns:
            dict: A dictionary with all the data needed to run the main script.
        """
        cache_path = self.cache_path / Path(f"{self.account}_cache.json")

        if container is None:
            container = {
                "data": list(data),
                "ignore": [],
                "history": [],
            }
        else:
            container["data"] = list(data)

        container["version"] = __version__
        container["date"] = datetime.now().isoformat()
        container["account"] = self.account

        with cache_path.open("w", encoding="utf-8") as file:
            json.dump(container, file)

        return container

    def convert_cache(self) -> None:
        def convert_old_cache(data: list[list]) -> set[str]:
            return [item[1] for item in data]

        cache_path = self.cache_path / Path("cache.json")

        if not cache_path.exists():
            return None

        log.info("Converting old cache.")
        log.warning("Cache conversion removed at a future time. Please report.")

        new_file = {
            "version": __version__,
            "account": self.account,
            "date": datetime.now().isoformat(),
        }
        with cache_path.open("r", encoding="utf-8") as file:
            cache_data = json.load(file)

        version = process_version(cache_data.get("version", "0.0.0"))

        if self.version > version:
            new_file["data"] = convert_old_cache(cache_data["data"])
        else:
            new_file["data"] = cache_data["data"]

        ignore_path = self.cache_path / Path("ignore.json")
        if ignore_path.exists():
            with ignore_path.open("r", encoding="utf-8") as file:
                ignore_list = json.load(file)
                new_file["ignore"] = convert_old_cache(ignore_list)

        selections_path = self.cache_path / Path("selections.json")
        if selections_path.exists():
            with selections_path.open("r", encoding="utf-8") as file:
                history = json.load(file)
                new_file["history"] = convert_old_cache(history)

        new_path = self.cache_path / Path(f"{self.account}_cache.json")
        with new_path.open("w", encoding="utf-8") as file:
            json.dump(new_file, file)

        if selections_path.exists():
            selections_path.unlink()

        if ignore_path.exists():
            ignore_path.unlink()

        cache_path.unlink()

        return None
