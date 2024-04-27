import random

import pytest
from github_random_star.__main__ import generate_cache_directory
from github_random_star.api import GithubAPI


@pytest.fixture(scope="session")
def cache_location():
    return generate_cache_directory()


@pytest.fixture(scope="session")
def set_user_settings():
    user = "ddkasa"
    max_values = 30
    max_history = 100
    return user, max_values, max_history


@pytest.fixture(scope="session")
def get_data(cache_location, set_user_settings):
    gh_api = GithubAPI(
        account=set_user_settings[0],
        cache_location=cache_location,
    )
    return gh_api.collect_starred_items()


@pytest.fixture(scope="session")
def set_seed():
    random.seed(0)
    yield
