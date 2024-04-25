import pytest

from github_random_star.__main__ import retrieve_cache


@pytest.mark.integration
def test_integration(set_user_settings, load_starred_items):
    user, max_results, _ = set_user_settings
    assert (
        len(
            retrieve_cache(
                user,
                refresh=True,
                max_results=max_results,
            )
        )
        == max_results
    )
