import sys
import logging

from cleo.application import Application
from cleo.io.inputs.string_input import StringInput

from github_random_star.__main__ import RandomStarCommand
from github_random_star.version import __version__


def run(args=None):
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    app = Application(
        name="Github Random Star",
        version=__version__,
    )
    cmd = RandomStarCommand()
    app.add(cmd)

    try:
        if args:
            input = StringInput(args)
            input.set_stream(sys.stdin)
            result = app.run(input, sys.stdout, sys.stderr)
        else:
            result = app.run()
    except (EOFError, KeyboardInterrupt):
        print("User Ended Session!")
        result = 0

    return result
