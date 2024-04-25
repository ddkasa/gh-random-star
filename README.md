# ⭐️ GitHub Random Star ⭐️

<a href="https://pypi.org/project/github-random-star"><img src="https://img.shields.io/pypi/v/github_random_star?style=for-the-badge&logo=pypi" /></a>
<a href=""><img src="https://img.shields.io/github/actions/workflow/status/ddkasa/github-random-star/pypi-publish.yml?style=for-the-badge"/></a>
<a href="https://pypi.org/project/github-random-star"><img src="https://img.shields.io/pypi/dm/github-random-star?style=for-the-badge" /></a>

![](docs/example_image.png?raw=true)

If you have starred way too many GitHub repositories and need a way of keeping track of them. This simple CLI tool throws you quasi random starred repos at you to look at and explore.

## Installation

### Preferred

Install with [Pipx](https://github.com/pypa/pipx).

`$ pipx install github-random-star`

### Other

Install from [PyPi](https://pypi.org/project/github-random-star)/[GitHub](https://github.com/ddkasa/github-random-star) with pip or clone this repository and install with pip/pipx locally.

## Usage

1. Setup GitHub API token as the `GITHUB_ACCESS_TOKEN` environment variable. _If this is not setup it will use the public access point with lower rates._
2. Run the script through `$ gh-star <flags>`, `$ python github_random_star/main.py <flags>` or if using Poetry `$ poetry run gh-star <flags>`

### Flags

- `-a, --account` Username of the GitHub account to retrieve the starred items from. `--account` is required or `GH_STAR_ACCOUNT` environment variable needs to be set.
- `-t, --total` Total amount of random items you want to pick from. Defaults to 3.
- `-r, --refresh` Whether to fetch new cached data or not. Will re fetch all starred items instead of using cache.
- `--max-history` The amount of historic choices to cache. Defaults to 100. Set to **-1** to keep history unlimited. `GH_STAR_MAX_HISTORY` environment variable can be used to override this value.
- `-i, --ignore` If to use a list of repositories to ignore. Defaults to true.
- `--max_results` The amount of starred items to retrieve from GitHub. Defaults to all.
- `-h --help` Show this help message inside the terminal.

### Examples

- `$ gh-star -a ddkasa`
- `$ gh-star -a ddkasa -t 5`
- `$ gh-star -a ddkasa -r -t 5`

## Development

Development is run through [Poetry](https://github.com/python-poetry/poetry).

### Basic Setup
1. `$ git clone https://github.com/ddkasa/github-random-star`
2. `$ cd github-random-star`
3. `$ poetry shell`
4. `$ poetry install`

### Testing
- Use `$ pytest` for all tests.
- Use `$ pytest -m unit` for unit tests.
- Use `$ pytest -m integration` for integration tests.

## License
MIT. Look at the [LICENSE](LICENSE.md) for details.
