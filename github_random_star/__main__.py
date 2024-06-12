from __future__ import annotations

import json
import logging
import os
import random
from typing import Any
import subprocess
from pathlib import Path

from cleo.application import Application
from cleo.commands.command import Command
from cleo.helpers import option, Option, Argument, argument
from cleo.io.outputs.output import Verbosity

from github_random_star.api import GithubAPI

log = logging.getLogger("GitHub Random Star")


class AccountMissingError(TypeError):
    "GitHub account was not provided through flags or an environment variable."


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


# REFACTOR: Compose into two objects separating the CLI and selection process.
class RandomStarCommand(Command):
    name = "star"
    description = "Fetch random starred repositories from GitHub Profile."
    arguments: list[Argument] = [
        argument(
            "account",
            description="Account to fetch starred repositories from.",
        )
    ]
    options: list[Option] = [
        option(
            "total",
            "t",
            "Total amount of random repositories you want to pick from.",
            flag=False,
            value_required=False,
            default=3,
        ),
        option(
            "refresh",
            "r",
            "Whether to fetch new cached data or not. Will re fetch all starred items instead of using cache.",
        ),
        option(
            "max_history",
            description="The amount of historic choices to cache. Set to -1 to keep history unlimited. GH_STAR_MAX_HISTORY environment variable can be used to override this value.",
            value_required=False,
            flag=False,
            default=100,
        ),
        option(
            "ignore",
            "i",
            "If to use a list of repositories to ignore. Defaults to true.",
        ),
        option(
            "max_results",
            description="The amount of starred items to retrieve from GitHub. Defaults to all.",
            value_required=False,
            flag=False,
            default=0,
        ),
    ]

    def option(self, name: str) -> Any:
        option = super().option(name)
        if name == "max_history" and option is None:
            option = int(os.environ.get("GH_STAR_MAX_HISTORY", 100))

        return option

    def handle(self) -> None:
        """Basic entrypoint for the CLI script."""
        cache_path = generate_cache_directory()

        token = os.environ.get("GITHUB_ACCESS_TOKEN")
        github_api = GithubAPI(
            self.argument("account"),
            cache_path,
            refresh=self.option("refresh"),
            max_results=self.option("max_results"),
            token=token,
        )
        starred_items = github_api.collect_starred_items()

        self.line(
            f"Total amount of starred items: {len(starred_items["data"])}",
            style="info",
        )

        data = self.item_selection(starred_items, cache_path)

        github_api.save_cached_items(data["data"], data)

        self.line("Done!", style="info")

    @staticmethod
    def extract_selection(path: Path) -> list[str]:
        """Extracts selections from JSON file.

        Args:
            path: Path to the JSON file.

        Returns:
            list(StarredItem): List of starred items from the JSON file. Needs to
                stay a list in order to preserve order when keeping history.
        """

        data: list[str] = []
        if path.exists():
            with path.open("r", encoding="utf-8") as file:
                selections = json.load(file)
                if "data" in selections:
                    selections = selections["data"]

        return data

    def user_selection(
        self,
        starred_items: set[str],
    ) -> tuple[str, float]:
        """Selection function where the user chooses a random starred item.

        Args:
            starred_items: Set of starred items from GitHub.

        Returns:
            tuple(StarredItem, float): Selected item and the selection number for
                further processing

        """
        total = self.option("total")
        items = random.sample(tuple(starred_items), total)

        self.line("Which repository would you like to view today?", style="question")
        self.line(
            "Note: Add .1 to number to add to ignore list",
            style="info",
            verbosity=Verbosity.VERBOSE,
        )
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

            self.line(
                f"Select an item within the range of 1 and {total}",
                style="error",
            )

        selected_item = items[int(selection - 1)]

        return selected_item, selection

    def item_selection(self, data: dict, cache_path: Path) -> dict[str, Any]:
        """Selection function where the user chooses a random starred item.

        Args:
            starred_items: Set of starred items from GitHub.
            cache_path: Path to the cache directory.

        Returns:
            dict: A dictionary with all the data to be cached to the JSON file.
        """

        starred_items = set(data["data"])

        max_history = self.option("max_history")
        ignore = not self.option("ignore")

        # TODO: Need a way of avoiding keeping enough items in the history.
        if max_history != -1:
            starred_items -= starred_items.intersection(set(data["history"]))

        if ignore:
            starred_items -= starred_items.intersection(set(data["ignore"]))

        selected_item, selection = self.user_selection(starred_items)

        gh_url = "https://github.com/" + selected_item

        log.info("Opening %s", gh_url)
        subprocess.run(
            ["python", "-m", "webbrowser", "-t", gh_url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if round(selection % 1, 1) == 0.1:
            self.line("Adding {selected_item} to ignore list", style="info")
            data["ignore"].append(selected_item)

        data["history"].insert(0, selected_item)
        if len(data["history"]) > max_history and max_history > 0:
            data["history"] = data["history"][: -(len(data["history"]) - max_history)]

        return data


if __name__ == "__main__":
    app = Application()
    app.add(RandomStarCommand())
    app.run()
