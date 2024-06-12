import fire

from .version import __version__
from .__main__ import main


__author__ = "David Kasakaits"
__version__ = __version__
__typed__ = True


def gh_star(*args, **kwargs) -> None:
    try:
        fire.Fire(main, *args, **kwargs)
    except EOFError:
        print("User exited the program!")
