import argparse
import asyncio
import sys

from pydantic import ValidationError

from . import __version__
from .settings import Settings


async def do_sample_command_1():
    """Run used defined command 1."""


async def do_sample_command_2():
    """Run user defined command 2."""


def main():
    parser = argparse.ArgumentParser(
        description="cat for jupyter notebooks",
        argument_default=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--list_field", help="Example of multi value list separated by comma.", type=str
    )
    parser.add_argument(
        "--version",
        help="Print version information and quite",
        action="version",
        version=__version__,
    )

    # Commands
    commands = parser.add_subparsers(title="Commands", dest="command")

    # Sample command 1
    sample_command_1 = commands.add_parser(
        "sample_command_1",
        help="Sample command description.",
        argument_default=argparse.SUPPRESS,
    )

    sample_command_1.set_defaults(func=do_sample_command_1)

    # Sample command 2
    sample_command_2 = commands.add_parser(
        "sample_command_2",
        help="Sample command description.",
        argument_default=argparse.SUPPRESS,
    )

    sample_command_2.set_defaults(func=do_sample_command_2)

    try:
        args = parser.parse_args()
        settings = Settings(**vars(args))
    except ValidationError as e:
        error = e.errors(include_url=False, include_context=False)[0]
        sys.exit(
            "Wrong argument value passed ({}): {}".format(
                error.get("loc", ("system",))[0], error.get("msg")
            )
        )

    if args.command:
        asyncio.run(args.func(settings))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
