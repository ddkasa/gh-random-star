import fire

from . import main as m


def main(*args, **kwargs) -> None:
    fire.Fire(m.main, *args, **kwargs)
