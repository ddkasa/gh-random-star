from abc import ABC
import json
import logging
from datetime import datetime
from pathlib import Path
import random
from typing import Any, Final, Optional

from httpx import Client, codes

from github_random_star.version import __version__, VersionNo

log = logging.getLogger("GitHub Random Star")


class GithubAPI(ABC):
    """API wrapper for the GitHub API.

    Handles fetching starred items from the GitHub API and cache.

    Methods:
        create_headers: Creates the headers for the API request.
        collect_items: Main method that run the the class.
        get_items: Fetches starred items from the API.
        load_items: Loads cached items from the cache.
        save_items: Formats saves cached items to a json file.

    Attributes:
        API_BASE_URL: Base URL for GitHub API.
        STARR_API_URL: URL endpoint template for fetching starred items.
        CACHE_PATH: Name of the cache file to seperate child commands.
        account: GitHub account name.
        cache_path: Path to the cache folder.
        refresh: Whether to refresh the cache.
        max_results: Maximum number of starred items to return.
        client: Persistent client for requests.
    """

    API_BASE_URL: Final[str] = "https://api.github.com/"
    USER_PARAMS: str = "users/{user}/"
    CACHE_PATH: str

    __slots__ = (
        "account",
        "cache_path",
        "refresh",
        "max_results",
        "client",
        "version",
    )

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
        self.cache_path = cache_location
        self.refresh = refresh
        self.max_results = max_results
        self.version = VersionNo.process_version(__version__)
        self.client = Client(
            headers=self.create_headers(token),
            base_url=self.API_BASE_URL,
            timeout=20,
        )

    def create_headers(self, token: Optional[str] = None) -> dict:
        headers = {"X-GitHub-Api-Version": "2022-11-28"}

        if token:
            log.info("Using provided GitHub API token")
            headers["Authorization"] = f"Bearer {token}"
        else:
            log.warning(
                "No GitHub API token provided. "
                "Using public access with a lower rate limit."
            )

        return headers

    def collect_items(self) -> dict[str, Any]:
        """Main method that runs the the class functionality.

        If the cache is valid, it will load it. Otherwise, it will request
        the data from the API and keep requesting until a page is not found or
        the maximum number of results is reached.

        Returns:
            dict: A dictionary with all the data needed to run the main script.
        """
        cache = self.load_items()
        if cache and not self.refresh:
            return cache

        log.info("Requesting data from Github")

        data = set()

        page = 1
        while True:
            log.debug("Requesting GH items page: %s", page)
            url = self.USER_PARAMS.format(user=self.account, page=page)
            response = self.request(url)
            if not response:
                break

            for item in response:
                data.add(item["full_name"])
                if self.max_results and len(data) >= self.max_results:
                    break

            if self.max_results and len(data) >= self.max_results:
                break

            page += 1
        return self.save_items(data, cache)

    def request(self, url: str, *, retry: bool = True) -> dict | None:
        response = self.client.get(url)

        if response.status_code != codes.OK:
            if retry and response.status_code == codes.INTERNAL_SERVER_ERROR:
                seconds = random.randint(1, 5)
                log.error(
                    "Server error: %s. Retrying in %s seconds.",
                    response.text,
                    seconds,
                )
                return self.request(url, retry=False)

            if (
                response.status_code == codes.TOO_MANY_REQUESTS
                or "rate limit exceeded" in response.text
            ):
                log.error(
                    "Rate limit exceeded. Stopping requests. %s",
                    response.text,
                )
                return None

            err = "Connection failed to get items for url %s. Status Code: %s"
            log.critical(err, url, response.status_code)
            response.raise_for_status()

        return response.json()

    def load_items(self) -> dict[str, Any] | None:
        cache_path = self.cache_path / Path(
            self.CACHE_PATH.format(account=self.account)
        )
        if not cache_path.exists():
            return None

        with cache_path.open("r", encoding="utf-8") as file:
            cache_data = json.load(file)

        log.info(
            "Cache last refreshed on the %s.",
            datetime.fromisoformat(cache_data["date"]).date().isoformat(),
        )

        version = VersionNo.process_version(cache_data.get("version", "0.0.0"))
        if self.version != version:
            log.warning(
                "Cache is from a different version. Current: %s - Stored: %s",
                __version__,
                version,
            )

        return self.save_items(cache_data.get("data", []), cache_data)

    def save_items(
        self,
        data: set[str],
        container: Optional[dict] = None,
    ) -> dict[str, Any]:
        """Formats saves cached items to a json file.

        Is meant to be used as a function as a tailed callback.

        Args:
            data: A set of repositories.
            container: A dictionary with all the data needed to run the main
                script.
        Returns:
            dict: A dictionary with all the data needed to run the main script.
        """
        cache_path = self.cache_path / Path(
            self.CACHE_PATH.format(account=self.account)
        )

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


class GHStars(GithubAPI):
    USER_PARAMS = GithubAPI.USER_PARAMS + "starred?page={page}&per_page=30"
    CACHE_PATH = "{account}_cache.json"


class GHRepos(GithubAPI):
    USER_PARAMS = GithubAPI.USER_PARAMS + "repos?page={page}&per_page=30"
    CACHE_PATH = "{account}_repo_cache.json"
