from __future__ import annotations

from cleo.application import Application
from .meta import BaseCommand


from github_random_star.api import GHStars


class StarCommand(BaseCommand):
    API = GHStars
    name = "star"
    description = "Fetch random starred repositories from a GitHub profile."


if __name__ == "__main__":
    app = Application()
    app.add(StarCommand())
    app.run()
