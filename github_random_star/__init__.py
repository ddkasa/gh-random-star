import fire

from . import main as m

__version__ = "0.0.3"


def main(*args, **kwargs) -> None:
    fire.Fire(m.main, *args, **kwargs)
