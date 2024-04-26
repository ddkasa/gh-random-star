from pathlib import Path

import pytest
import mock
import builtins

from github_random_star.__main__ import item_selection


@pytest.mark.unit
def test_cache_path(cache_location):
    assert isinstance(cache_location, Path)
    assert cache_location.exists()


@pytest.mark.unit
def test_file_load(load_starred_items):
    assert load_starred_items


@pytest.mark.unit
def test_random_selection(set_seed, load_starred_items, cache_location):
    with mock.patch.object(builtins, "input", lambda _: 2):
        assert (
            item_selection(
                set(load_starred_items), cache_location, total=3, max_history=-1
            )
            is None
        )
