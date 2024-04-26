from pathlib import Path

import json

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
                set(load_starred_items),
                cache_location,
                total=3,
                max_history=-1,
            )
            is None
        )


@pytest.mark.unit
def test_ignore_file(set_seed, load_starred_items, cache_location):
    ignore_file = cache_location / Path("ignore.json")
    with ignore_file.open("r", encoding="utf-8") as file:
        pre_len = len(json.load(file))

    with mock.patch.object(builtins, "input", lambda _: 2.1):
        assert (
            item_selection(
                set(load_starred_items),
                cache_location,
                total=3,
                max_history=-1,
            )
            is None
        )

    with ignore_file.open("r", encoding="utf-8") as file:
        post_len = len(json.load(file))
    assert post_len - 1 == pre_len
