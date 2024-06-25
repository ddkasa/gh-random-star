# ⭐️ GitHub Random Star ⭐️

<a href="https://pypi.org/project/github-random-star"><img src="https://img.shields.io/pypi/v/github_random_star?style=for-the-badge&logo=pypi" /></a>
<a href=""><img src="https://img.shields.io/github/actions/workflow/status/ddkasa/github-random-star/pypi-publish.yml?style=for-the-badge"/></a>
<a href="https://pypi.org/project/github-random-star"><img src="https://img.shields.io/pypi/dm/github-random-star?style=for-the-badge" /></a>

![](docs/example_image.png?raw=true)

If you have starred way too many GitHub repositories and need a way of keeping track of them. This simple CLI tool throws you quasi random starred repos at you to look at and explore.

If you are struggling with selection paralysis; it also allows for selecting random repositories from a GitHub user.

## Installation

### Preferred

#### Install with [Pipx](https://github.com/pypa/pipx) or Pip.

```
pipx install github-random-star
```

#### Install with [GitHub CLI](https://github.com/cli/cli).

```
gh extension install ddkasa/github-random-star
```

## Usage

- Setup GitHub API token as the `GITHUB_TOKEN` environment variable. _If this is not setup it will use the public access point with lower rates._

### PyPi
- Run the script through `gh-star <command> <account> <flags>`.
- Run `gh-star help star` to get help.

### GitHub CLI
- Run the script through `gh random-star <command> <account> <flags>`.
- Run `gh random-star help star` to get help.

### Commands
1. `star` Randomly select from all starred items of a GH user.
2. `repo` Randomly select from a GH users repositories.

### Arguments
- `<account>` Username of the GitHub account to retrieve the starred items from. **Required**

### Flags

- `-t, --total` Total amount of random items you want to pick from. Defaults to 3.
- `-r, --refresh` Whether to fetch new cached data or not. Will re fetch all starred items instead of using cache.
- `--max-history` The amount of historic choices to cache. Defaults to 100. Set to **-1** to keep history unlimited. `GH_STAR_MAX_HISTORY` environment variable can be used to override this value.
- `-i, --ignore` If to use a list of repositories to ignore. Defaults to true.
- `--max_results` The amount of starred items to retrieve from GitHub. Defaults to all.

### Examples

- `gh-star star ddkasa`
- `gh-star repo ddkasa`
- `gh-star star ddkasa -t 5`
- `gh-star star ddkasa -r -t 5`
- `gh random-star star ddkasa`
- `gh random-star repo ddkasa`

## Development

Development is run through [Poetry](https://github.com/python-poetry/poetry).

### Basic Setup
1. `git clone https://github.com/ddkasa/github-random-star`
2. `cd github-random-star`
3. `poetry shell`
4. `poetry install`

### Testing
- Use `pytest` for all tests.
- Use `pytest -m unit` for unit tests.
- Use `pytest -m integration` for integration tests.

## License
MIT. Look at the [LICENSE](LICENSE.md) for details.
