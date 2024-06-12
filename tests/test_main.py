import builtins
from pathlib import Path
import json

import mock
import pytest
from cleo.application import Application
from cleo.testers.command_tester import CommandTester
from github_random_star.__main__ import RandomStarCommand


@pytest.mark.unit
def test_cache_path(cache_location):
    assert isinstance(cache_location, Path)
    assert cache_location.exists()


@pytest.mark.unit
def test_random_selection(set_seed, cache_location, get_data, set_user_settings):
    app = Application()
    cmd = RandomStarCommand()
    app.add(cmd)

    command = app.find("star")
    tester = CommandTester(command)

    with mock.patch.object(builtins, "input", lambda _: 2):
        assert tester.execute(set_user_settings[0]) == 0


@pytest.mark.unit
def test_ignore_file(set_seed, cache_location, set_user_settings, get_data):
    user, max_results, _ = set_user_settings
    pre_len = len(get_data["ignore"])
    app = Application()
    cmd = RandomStarCommand()
    app.add(cmd)

    command = app.find("star")
    tester = CommandTester(command)

    with mock.patch.object(builtins, "input", lambda _: 2.1):
        assert tester.execute(f"{user} --max_results {max_results}") == 0

    cl = cache_location / f"{user}_cache.json"
    with cl.open() as f:
        post_len = len(json.load(f)["ignore"])

    assert post_len - 1 == pre_len
