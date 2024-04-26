import pytest
from github_random_star.api import GithubAPI


@pytest.mark.integration
def test_integration(
    set_user_settings,
    load_starred_items,
    cache_location,
):
    user, max_results, _ = set_user_settings
    gh_api = GithubAPI(
        account=user,
        cache_location=cache_location,
        refresh=True,
        max_results=max_results,
    )

    assert len(gh_api.collect_starred_items()) == max_results
