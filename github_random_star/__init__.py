import fire  # type: ignore[import-not-found]

from .__main__ import main

__version__ = "0.0.5"


def gh_star(*args, **kwargs) -> None:
    try:
        fire.Fire(main, *args, **kwargs)
    except EOFError:
        print("User exited the program!")
