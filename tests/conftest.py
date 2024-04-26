import random
from pathlib import Path

import pytest
from github_random_star.__main__ import extract_selection, generate_cache_directory


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
def load_starred_items():
    test_path = Path("tests/files/load_test.json")
    return extract_selection(test_path)


@pytest.fixture(scope="session")
def set_seed():
    random.seed(0)
    yield
