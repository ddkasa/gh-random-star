import fire

from .version import __version__
from .__main__ import main

__version__ = __version__


def gh_star(*args, **kwargs) -> None:
    try:
        fire.Fire(main, *args, **kwargs)
    except EOFError:
        print("User exited the program!")
