import json
import logging as log
import os
import random
from typing import Optional

import fire
import httpx

USER_API_URL = "https://api.github.com/users/{user}/starred?page={page}&per_page=30"


def main(account: Optional[str] = None, total: int = 1) -> None:
    log.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=log.INFO,
    )
    log.info("Requesting Data from Github")

    if account is None:
        account = os.environ.get("GITHUB_ACCOUNT")
        if account is None:
            raise ValueError(
                "Account not provided from arguments or environment variables."
            )

    os.environ.get("GITHUB_ACCESS_TOKEN")

    formatted_url = USER_API_URL.format(user=account, page=1)

    request = httpx.get(formatted_url, timeout=20)

    if request.status_code != 200:
        raise ConnectionError(
            "Connection failed to get starred items for {account}.\
             Status Code: {request.status_code}"
        )

    data = request.json()

    with open("data.json", "w") as file:
        file.write(json.dumps(data))

    log.info("Total amount of arguments: %s", len(data))


if __name__ == "__main__":
    fire.Fire(main)
