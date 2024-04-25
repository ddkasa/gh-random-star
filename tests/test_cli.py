import subprocess

import pytest


@pytest.mark.unit
def test_cli(set_user_settings):
    process = subprocess.Popen(
        ["gh-star", "-a", set_user_settings[0], "--total", "3"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    out, _ = process.communicate(input=b"1")

    assert process.returncode == 0
