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
    <code>$ poetry shell</code><br>
    <code>$ poetry install</code>
</details>
<details>
    <summary> If using requirements.txt.</summary>
    <code>$ virtualenv -p python3.12 .venv</code><br>
    <code>$ source .venv/bin/activate</code><br>
    <code>$ pip install -r requirements.txt</code>
</details>

# Usage

1. Setup GitHub API token as the `GITHUB_ACCESS_TOKEN` environment variable. _If this is not setup it will use the public access point with lower rates._
2. Run the script through `gh-star <flags>`, `python github_random_star/main.py <flags>` or if using poetry `poetry run gh-star <flags>`

## Flags

- `-a, --account` Username of the GitHub account to retrieve the starred items from. `--account` is required or `GH_STAR_ACCOUNT` environment variable needs to be set.
- `-t, --total` Total amount of random items to pick from. Defaults to 3.
- `-r, --refresh` Whether to fetch new cached data or not. Will re fetch all starred items instead of using cache.
- `-m, --max-history` The amount of historic choices to cache. Defaults to 100. Set to -1 to keep history unlimited. `GH_STAR_MAX_HISTORY` environment variable can be used to override this value.
- `-i, --ignore` If to use a list of repositories to ignore. Defaults to true.

## Examples

- `gh-star -a ddkasa`
- `gh-star -a ddkasa -t 5`
- `gh-star -a ddkasa -r -t 5`

# License

MIT. Look at the [LICENSE](LICENSE.md) for details.
