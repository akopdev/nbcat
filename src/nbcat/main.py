import argparse
import base64
import sys
from pathlib import Path

import argcomplete
import requests
from argcomplete.completers import FilesCompleter
from markdownify import markdownify
from pydantic import ValidationError
from rich.console import Console, Group, RenderableType
from rich.padding import Padding
from rich.panel import Panel
from rich.pretty import Pretty
from rich.syntax import Syntax
from rich.text import Text

from nbcat.image import render_image

from . import __version__
from .enums import CellType, OutputCellType
from .exceptions import (
    InvalidNotebookFormatError,
    NotebookNotFoundError,
    UnsupportedNotebookTypeError,
)
from .markdown import Markdown
from .pager import Pager
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


def render_cell(cell: Cell) -> RenderableType:
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
        return Markdown(markdownify(input), code_theme="ansi_dark")

    def _render_code(input: str, language: str = "python") -> Syntax:
        return Syntax(input, language, theme="ansi_dark", padding=(1, 2), dedent=True)

    def _render_raw(input: str) -> Text:
        return Text(input)

    def _render_image(input: str) -> RenderableType:
        return render_image(base64.b64decode(input.replace("\n", "")))

    def _render_json(input: str) -> Pretty:
        return Pretty(input)

    RENDERERS = {
        CellType.MARKDOWN: _render_markdown,
        CellType.CODE: _render_code,
        CellType.RAW: _render_raw,
        CellType.HEADING: _render_markdown,
        OutputCellType.PLAIN: _render_raw,
        OutputCellType.HTML: _render_markdown,
        OutputCellType.IMAGE: _render_image,
        OutputCellType.JSON: _render_json,
    }

    rows: list[RenderableType] = []
    renderer = RENDERERS.get(cell.cell_type)
    source = renderer(cell.input) if renderer else None
    if source:
        s_title = f"[green]In [{cell.execution_count}][/]" if cell.execution_count else None
        if s_title:
            rows.append(Panel(source, title=s_title, title_align="left"))
        else:
            rows.append(Padding(source, (1, 0)))

        if not cell.outputs:
            return rows.pop()

    for o in cell.outputs:
        o_title = f"[blue]Out [{o.execution_count}][/]" if o.execution_count else None
        if o.output:
            renderer = RENDERERS.get(o.output.output_type)
            output = renderer(o.output.text) if renderer else None
            if output:
                if o_title:
                    rows.append(Panel(output, style="italic", title=o_title, title_align="left"))
                else:
                    rows.append(Padding(output, (1, 0), style="italic"))
    return Group(*rows)


def render_notebook(nb: Notebook) -> list[RenderableType]:
    """
    Convert a Notebook object into a list of rich renderables for terminal display.

    Each cell in the notebook is processed and rendered using `render_cell`,
    producing a sequence of styled input/output blocks suitable for use in a
    Textual or Rich-based terminal UI.

    Args:
        nb (Notebook): The notebook object containing parsed cells (e.g., from a .ipynb file).

    Returns
    -------
        list[RenderableType]: A list of rich renderable objects representing the notebook cells.
                              Returns an empty list if the notebook has no cells.
    """
    rendered: list[RenderableType] = []
    for cell in nb.cells:
        rendered.append(render_cell(cell))
    return rendered


def main():
    parser = argparse.ArgumentParser(
        description="cat for Jupyter Notebooks",
        argument_default=argparse.SUPPRESS,
    )
    parser.add_argument(
        "file", help="Path or URL to a .ipynb notebook", type=str
    ).completer = FilesCompleter()
    parser.add_argument(
        "-v",
        "--version",
        help="print version information and quite",
        action="version",
        version=__version__,
    )
    parser.add_argument(
        "-d", "--debug", help="enable extended error output", action="store_true", default=False
    )
    parser.add_argument(
        "-p",
        "--page",
        help="enable paginated view mode (similar to less)",
        action="store_true",
        default=False,
    )

    try:
        argcomplete.autocomplete(parser)
        args = parser.parse_args()

        notebook = read_notebook(args.file, debug=args.debug)
        objects = render_notebook(notebook)

        if not objects:
            console.print("[bold red]Notebook contains no cells.")
            return

        if args.page:
            Pager(objects).run()
        else:
            console.print(*objects)
    except Exception as e:
        sys.exit(f"nbcat: {e}")


if __name__ == "__main__":
    main()
