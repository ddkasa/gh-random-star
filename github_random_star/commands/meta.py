from __future__ import annotations

import json
import logging
import os
import random
from typing import Any, Final
import subprocess
from pathlib import Path

from cleo.commands.command import Command
from cleo.helpers import option, Option, Argument, argument
from cleo.io.outputs.output import Verbosity

from github_random_star.api import GithubAPI
from github_random_star.utility import generate_cache_directory


log = logging.getLogger("GitHub Random Star")


class BaseCommand(Command):
    GH_URL: Final[str] = "https://github.com/"
    API: type[GithubAPI]

    arguments: list[Argument] = [
        argument(
            "account",
            description="Account to fetch data from.",
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
            "Whether to fetch new cached data or not. Will re-fetch all repositories instead of using cache.",
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
            description="The max amount of items to retrieve from GitHub. Defaults to all.",
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

        github_api = self.API(
            self.argument("account"),
            cache_path,
            refresh=self.option("refresh"),
            max_results=self.option("max_results"),
            token=os.environ.get("GITHUB_ACCESS_TOKEN"),
        )
        repositories = github_api.collect_items()

        self.line(
            f"Total amount of repositories: {len(repositories["data"])}",
            style="info",
        )

        data = self.item_selection(repositories, cache_path)

        github_api.save_items(data["data"], data)

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
        raw_items: set[str],
    ) -> tuple[str, float]:
        """Selection function where the user chooses a random repository.

        Args:
            starred_items: Set of starred items from GitHub.

        Returns:
            tuple[str, float]: Selected item and the selection number for
                further processing

        """
        total = self.option("total")
        items = random.sample(tuple(raw_items), total)

        self.line("Which repository would you like to view today?", style="question")
        self.line(
            "Note: Add .1 to number to add to ignore list",
            style="info",
            verbosity=Verbosity.VERBOSE,
        )
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
        """Selection function where the user chooses a repository.

        Args:
            items: Set of items from GitHub.
            cache_path: Path to the cache directory.

        Returns:
            dict: A dictionary with all the data to be cached to the JSON file.
        """

        items = set(data["data"])

        max_history = self.option("max_history")
        ignore = not self.option("ignore")

        # TODO: Need a way of avoiding keeping enough items in the history.
        if max_history != -1:
            items -= items.intersection(set(data["history"]))

        if ignore:
            items -= items.intersection(set(data["ignore"]))

        selected_item, selection = self.user_selection(items)

        gh_url = self.GH_URL + selected_item

        log.info("Opening %s", gh_url)
        subprocess.run(
            ["python", "-m", "webbrowser", "-t", gh_url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if round(selection % 1, 1) == 0.1:
            self.line(f"Adding {selected_item} to ignore list", style="info")
            data["ignore"].append(selected_item)

        data["history"].insert(0, selected_item)
        if len(data["history"]) > max_history and max_history > 0:
            data["history"] = data["history"][: -(len(data["history"]) - max_history)]

        return data
