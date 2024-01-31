import logging as log
import sys
from typing import Optional

import fire
import httpx


def main(github_account: Optional[str] = None, total: int = 1) -> None:
    log.info("Requesting Data from Github")


if __name__ == "__main__":
    fire.Fire(main)
