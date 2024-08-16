import builtins
import json
from pathlib import Path

import mock  # type: ignore[import]
import pytest
from cleo.application import Application
from cleo.testers.command_tester import CommandTester
from github_random_star.commands import RepoCommand, StarCommand


@pytest.mark.unit
def test_cache_path(cache_location):
    assert isinstance(cache_location, Path)
    assert cache_location.exists()


@pytest.mark.unit
def test_random_selection(set_seed, cache_location, get_data, set_user_settings):
    app = Application()
    cmd = StarCommand()
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
    cmd = StarCommand()
    app.add(cmd)

    command = app.find("star")
    tester = CommandTester(command)

    with mock.patch.object(builtins, "input", lambda _: 2.1):
        assert tester.execute(f"{user} --max_results {max_results}") == 0

    cl = cache_location / f"{user}_cache.json"
    with cl.open() as f:
        post_len = len(json.load(f)["ignore"])

    assert post_len - 1 == pre_len


@pytest.mark.unit
def test_filter_data(capsys, monkeypatch):
    app = Application()
    app.add(RepoCommand())

    cmd = app.find("repo")

    monkeypatch.setattr(cmd, "option", lambda x: True)

    monkeypatch.setattr(
        cmd,
        "line",
        lambda *_, **__: print("History too long. Clearing..."),
    )

    data = {
        "data": [
            "ddkasa/gh-random-star",
            "ddkasa/ulauncher-toggl-extension",
            "ddkasa/Aoe4bot",
        ],
        "ignore": [],
        "history": ["wadawd", "awdawd", "wadwadaw"],
    }

    cmd._filter_data(data, 3)

    out, err = capsys.readouterr()

    assert "History too long. Clearing.." in out
    assert "" == err
    assert len(data["history"]) == 0
