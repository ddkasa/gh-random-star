import pytest
from github_random_star.api import GHStars


@pytest.mark.integration
def test_integration(set_user_settings, cache_location):
    user, max_results, _ = set_user_settings
    gh_api = GHStars(
        account=user,
        cache_location=cache_location,
        refresh=True,
        max_results=max_results,
    )
    data = gh_api.collect_items()
    assert len(data) <= max_results
