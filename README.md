# ⭐️ GitHub Random Star ⭐️

# Idea

I generally have starred way too many repository. I wanted to create a simple CLI tool that throws me one random repo I have starred once a day, so I can go back to these repos and explore them more in detail.

# Installation

## Preferred

Install through [Pipx](https://github.com/pypa/pipx) from PyPi.

`pipx install github-random-star`

## Other

Either install from [pypi](https://pypi.org/project/github-random-star) with `pip` or clone this repository and install requirements through [poetry](pyproject.toml) or the provided [requirements](requirements.txt) file.

<details>
    <summary>If using poetry.</summary>
    ```
    $ poetry shell
    $ poetry install
    ```
</details>
<details>
    <summary> If using requirements.txt.</summary>
    ```
    $ virtualenv -p python3.12 .venv
    $ source .venv/bin/activate
    $ pip install -r requirements.txt
    ```
</details>

# Usage

1. Setup GitHub API token as the `GITHUB_ACCESS_TOKEN` environment variable. _If this is not setup it will use the public access point with lower rates._
2. Run the script through `gh-star <flags>`, `python github_random_star/main.py <flags>` or if using poetry `poetry run gh-star <flags>`

## Flags

- `-a, --account` Username of the github account to retrieve the starred items from. `--account` is required or `GITHUB_ACCOUNT` environment variable needs to be set.
- `-t, --total` Total amount of random items to pick from. Defaults to 3.
- `-r, --refresh` Whether to fetch new cached data or not. Will refetch all starred items.
- `-m, --max-history` The amount of historic choices to cache. Defaults to 100.

# License

MIT. Look at the [LICENSE](LICENSE.md) for details.
