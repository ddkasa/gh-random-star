# GitHub Random Star

# Idea

I generally have starred way too many repository. I wanted to create a CLI tool that throws me one random repo I have starred once a day, so I can go back to these repos and explore them.

# Installation

## Preferred

Install through [Pipx](https://github.com/pypa/pipx) from PyPi.

`pipx install github-random-star`

## Other

Either install from [pypi](https://pypi.org/project/github-random-star) with `pip/pipx` or clone this repository and install requirements through [poetry](pyproject.toml) or the provided [requirements](requirements.txt) file.

```
# If using poetry.
$ poetry shell
$ poetry install
```

```
# If using requirements
$ virtualenv -p python3.12 .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

2. Setup GitHub API token as the `GITHUB_ACCESS_TOKEN` environment variable. _If this is not setup it will use the public access point with lower rates._

# Usage

Run the script through, `gh-star <flags>`, `python github_random_star/main.py <flags>` or if using poetry `poetry run gh-star <flags>`

## Flags

- `-a, --account` Username of the github account to retrieve the starred items from.
- `-t, --total` Total amount of random items to pick.
- `-r, --refresh` Whether to fetch new cached data or not.
- `-m, --max-history` The amount of historic choices to cache.

# License

MIT. Look at the [LICENSE](LICENSE.md) for details.
