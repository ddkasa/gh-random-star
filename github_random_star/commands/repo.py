from .meta import BaseCommand

from github_random_star.api import GHRepos


class RepoCommand(BaseCommand):
    API = GHRepos
    name = "repo"
    description = "Fetch random repositories from a GitHub user."
