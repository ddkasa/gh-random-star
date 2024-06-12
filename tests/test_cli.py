import subprocess

import pytest


@pytest.mark.unit()
def test_cli(set_user_settings):
    process = subprocess.Popen(
        ["gh-star", "star", set_user_settings[0], "--total", "3"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    out, _ = process.communicate(input=b"1")

    assert process.returncode == 1


@pytest.mark.integration()
def test_cli_integration(set_user_settings):
    process = subprocess.Popen(
        [
            "gh-star",
            "star",
            set_user_settings[0],
            "--refresh",
            "--max_results",
            str(set_user_settings[2]),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    out, _ = process.communicate(input=b"1.1")
    print(process.stderr)

    assert process.returncode == 1
