import random
import os

import pytest
from github_random_star.__main__ import generate_cache_directory
from github_random_star.api import GHStars


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
    gh_api = GHStars(
        account=set_user_settings[0],
        cache_location=cache_location,
        max_results=set_user_settings[1],
        token=os.environ.get("GITHUB_ACCESS_TOKEN"),
    )
    return gh_api.collect_items()


@pytest.fixture(scope="session")
def set_seed():
    random.seed(0)
    yield
