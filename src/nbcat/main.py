import argparse
import sys
from pathlib import Path

import argcomplete
import requests
from argcomplete.completers import FilesCompleter
from pydantic import ValidationError
from rich import box
from rich.console import Console, RenderableType
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from . import __version__
from .enums import CellType
from .exceptions import (
    InvalidNotebookFormatError,
    NotebookNotFoundError,
    UnsupportedNotebookTypeError,
)
from .schemas import Cell, Notebook

console = Console()


def read_notebook(fp: str, debug: bool = False) -> Notebook:
    """
    Load and parse a Jupyter notebook from a local file or remote URL.

    Args:
        fp (str): Path to a local `.ipynb` file or a URL pointing to a notebook.

    Returns
    -------
        Notebook: A validated Notebook instance parsed from JSON content.

    Raises
    ------
        NotebookNotFoundError: If the file path or URL is unreachable.
        UnsupportedNotebookTypeError: If the file exists but isn't a `.ipynb` file.
        InvalidNotebookFormatError: If the file content is invalid JSON or doesn't match schema.
    """
    path = Path(fp)
    if path.exists():
        if path.suffix != ".ipynb":
            raise UnsupportedNotebookTypeError(f"Unsupported file type: {path.suffix}")
        content = path.read_text(encoding="utf-8")
    elif fp.startswith("http://") or fp.startswith("https://"):
        try:
            with requests.Session() as req:
                res = req.get(fp, timeout=5)
                res.raise_for_status()
                content = res.text
        except requests.RequestException as e:
            raise NotebookNotFoundError(f"Unable to fetch remote notebook: {e}")
    else:
        raise NotebookNotFoundError(f"Notebook not found: {fp}")
    try:
        return Notebook.model_validate_json(content)
    except ValidationError as e:
        if not debug:
            raise InvalidNotebookFormatError("Failed to read notebook")
        raise InvalidNotebookFormatError(f"Invalid notebook: {e}")


def render_cell(cell: Cell) -> list[tuple[str | None, RenderableType]]:
    """
    Render the content of a notebook cell for display.

    Depending on the cell type, the function returns a formatted object
    that can be rendered in a terminal using the `rich` library.

    Args:
        cell (Cell): The notebook cell containing source content and type metadata.

    Returns
    -------
        Markdown | Panel | Text | None: A Rich renderable for Markdown, Code, or Raw cells.
        Returns None if the cell type is unrecognized or unsupported.
    """

    def _render_markdown(input: str) -> Markdown:
        return Markdown(input)

    def _render_code(input: str) -> Panel:
        return Panel(Syntax(input, "python", theme="ansi_dark"), box=box.SQUARE)

    def _render_raw(input: str) -> Text:
        return Text(input)

    RENDERERS = {
        CellType.MARKDOWN: _render_markdown,
        CellType.CODE: _render_code,
        CellType.RAW: _render_raw,
        CellType.HEADING: _render_markdown,
    }

    rows: list[tuple[str | None, RenderableType]] = []
    renderer = RENDERERS.get(cell.cell_type)
    source = renderer(cell.input) if renderer else None
    if source:
        label = f"[green][{cell.execution_count}][/]:" if cell.execution_count else None
        rows.append(
            (
                label,
                source,
            )
        )

    for o in cell.outputs:
        if o.output:
            label = f"[blue][{o.execution_count}][/]:" if o.execution_count else None
            rows.append(
                (
                    label,
                    o.output,
                )
            )
    return rows


def print_notebook(nb: Notebook):
    """
    Print the notebook to the console with formatted cell inputs and outputs.

    Args:
        nb (Notebook): A Notebook object containing a list of cells.
    """
    if not nb.cells:
        console.print("[bold red]Notebook contains no cells.")
        return

    layout = Table.grid(padding=1)
    layout.add_column(no_wrap=True, width=6)
    layout.add_column()

    for cell in nb.cells:
        for label, content in render_cell(cell):
            layout.add_row(label, content)

    console.print(layout)


def main():
    parser = argparse.ArgumentParser(
        description="cat for Jupyter Notebooks",
        argument_default=argparse.SUPPRESS,
    )
    parser.add_argument(
        "file", help="Path or URL to a .ipynb notebook", type=str
    ).completer = FilesCompleter()
    parser.add_argument(
        "--version",
        help="print version information and quite",
        action="version",
        version=__version__,
    )
    parser.add_argument(
        "--debug", help="enable extended error output", action="store_true", default=False
    )

    try:
        argcomplete.autocomplete(parser)
        args = parser.parse_args()
        notebook = read_notebook(args.file, debug=args.debug)
        print_notebook(notebook)
    except Exception as e:
        sys.exit(f"nbcat: {e}")


if __name__ == "__main__":
    main()
