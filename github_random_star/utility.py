from __future__ import annotations

import logging
import os
from pathlib import Path


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
