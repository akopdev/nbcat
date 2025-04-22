import argparse
import sys

from pydantic import ValidationError

from . import __version__
from .nbcat import Nbcat


def main():
    parser = argparse.ArgumentParser(
        description="cat for Jupyter Notebooks",
        argument_default=argparse.SUPPRESS,
    )
    parser.add_argument("file", help="Path or URL to a .ipynb notebook", type=str)
    parser.add_argument(
        "--version",
        help="print version information and quite",
        action="version",
        version=__version__,
    )

    try:
        args = parser.parse_args()
        nbcat = Nbcat(args.file)
        nbcat.print()
    except ValidationError as e:
        sys.exit(f"nbcat: Invalid notebook: {e}")
    except Exception as e:
        sys.exit(f"nbcat: {e}")


if __name__ == "__main__":
    main()
