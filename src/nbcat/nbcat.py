import os
import urllib.request
from pathlib import Path

from pydantic import AnyHttpUrl, ValidationError


from rich import box
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.console import Console
from rich.table import Table

from nbcat.enums import CellType
from nbcat.schemas import Notebook, Cell
from rich.text import Text


class Nbcat:
    def __init__(self, filename: str, theme: str = "ansi_dark") -> None:
        self.theme = theme
        if not os.path.isfile(filename):
            try:
                self.file = AnyHttpUrl(url=filename)
            except ValidationError:
                raise Exception(f"{filename}: No such file or directory.")
        else:
            self.file = filename

    def read(self, source: str | AnyHttpUrl) -> Notebook:
        if isinstance(source, AnyHttpUrl):
            with urllib.request.urlopen(str(source)) as response:
                content = response.read().decode("utf-8")
        else:
            content = Path(source).read_text(encoding="utf-8")
        return Notebook.model_validate_json(content)

    def render_source(self, cell: Cell):
        if cell.cell_type == CellType.MARKDOWN:
            return Markdown(cell.input)
        elif cell.cell_type == CellType.CODE:
            return Panel(
                Syntax(cell.input, "python", line_numbers=True, theme=self.theme), box=box.SQUARE
            )
        elif cell.cell_type == CellType.RAW:
            return Text(cell.input)

    def print(self):
        nb = self.read(self.file)
        console = Console()
        layout = Table.grid(padding=1)
        layout.add_column(no_wrap=True)
        layout.add_column()
        for cell in nb.cells:
            source = self.render_source(cell)
            layout.add_row(
                f"In [{cell.execution_count}]:" if cell.execution_count else None, source
            )
            if cell.output:
                layout.add_row(
                    f"Out [{cell.execution_count}]:" if cell.execution_count else None, cell.output
                )
        console.print(layout)
