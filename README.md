# ⭐️ GitHub Random Star ⭐️

<a href="https://pypi.org/project/github-random-star"><img src="https://img.shields.io/pypi/v/github_random_star?style=for-the-badge&logo=pypi" /></a>
<a href="https://pypi.org/project/github-random-star"><img src="https://img.shields.io/pypi/dm/github-random-star?style=for-the-badge" /></a>

![](docs/example_image.png?raw=true)

If you have starred way too many GitHub repositories and need a way of keeping track of them. This simple CLI tool throws you quasi random starred repos to look at and explore.

## Installation

### Preferred

Install with [Pipx](https://github.com/pypa/pipx).

`pipx install github-random-star`

### Other

Install from [PyPi](https://pypi.org/project/github-random-star)/[GitHub](https://github.com/ddkasa/github-random-star) with `pip` or clone this repository and install requirements through [Poetry](pyproject.toml) or the provided [requirements](requirements.txt) file.

<details>
    <summary>If using poetry.</summary>
    <code>$ git clone https://github.com/ddkasa/github-random-star</code><br>
    <code>$ cd github-random-star</code><br>
    <code>$ poetry shell</code><br>
    <code>$ poetry install</code>
</details>
<details>
    <summary>If using requirements.txt.</summary>
    <code>$ git clone https://github.com/ddkasa/github-random-star</code><br>
    <code>$ cd github-random-star</code><br>
    <code>$ virtualenv -p python3.12 .venv</code><br>
    <code>$ source .venv/bin/activate</code><br>
    <code>$ pip install -r requirements.txt</code>
</details>

## Usage

1. Setup GitHub API token as the `GITHUB_ACCESS_TOKEN` environment variable. _If this is not setup it will use the public access point with lower rates._
2. Run the script through `gh-star <flags>`, `python github_random_star/main.py <flags>` or if using poetry `poetry run gh-star <flags>`

### Flags

- `-a, --account` Username of the GitHub account to retrieve the starred items from. `--account` is required or `GH_STAR_ACCOUNT` environment variable needs to be set.
- `-t, --total` Total amount of random items you want to pick from. Defaults to 3.
- `-r, --refresh` Whether to fetch new cached data or not. Will re fetch all starred items instead of using cache.
- `-m, --max-history` The amount of historic choices to cache. Defaults to 100. Set to **-1** to keep history unlimited. `GH_STAR_MAX_HISTORY` environment variable can be used to override this value.
- `-i, --ignore` If to use a list of repositories to ignore. Defaults to true.

### Examples

- `gh-star -a ddkasa`
- `gh-star -a ddkasa -t 5`
- `gh-star -a ddkasa -r -t 5`

## License

MIT. Look at the [LICENSE](LICENSE.md) for details.
