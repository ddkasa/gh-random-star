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
def test_random_selection(set_seed, cache_location, get_data):
    with mock.patch.object(builtins, "input", lambda _: 2):
        assert isinstance(
            item_selection(
                get_data,
                cache_location,
                total=3,
                max_history=-1,
            ),
            dict,
        )


@pytest.mark.unit
def test_ignore_file(set_seed, cache_location, set_user_settings, get_data):
    user, max_results, _ = set_user_settings
    pre_len = len(get_data["ignore"])

    with mock.patch.object(builtins, "input", lambda _: 2.1):
        sel = item_selection(
            get_data,
            cache_location,
            total=3,
            max_history=-1,
        )

    post_len = len(sel["ignore"])

    assert post_len - 1 == pre_len
