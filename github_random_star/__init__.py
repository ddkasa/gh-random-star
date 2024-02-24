import fire  # type: ignore[import-not-found]

from . import main as m

__version__ = "0.0.4"


def main(*args, **kwargs) -> None:
    fire.Fire(m.main, *args, **kwargs)
