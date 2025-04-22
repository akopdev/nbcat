import os
import urllib.request
from pathlib import Path


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
        self.file = filename

    def read(self, source: str) -> Notebook:
        if os.path.isfile(source):
            content = Path(source).read_text(encoding="utf-8")
        else:
            with urllib.request.urlopen(str(source)) as response:
                content = response.read().decode("utf-8")
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
        layout.add_column(no_wrap=True, width=5)
        layout.add_column()
        for cell in nb.cells:
            source = self.render_source(cell)
            layout.add_row(f"[{cell.execution_count}]:" if cell.execution_count else None, source)
            if cell.outputs:
                for o in cell.outputs:
                    if o.output:
                        layout.add_row(
                            f"[{o.execution_count}]:" if o.execution_count else None, o.output
                        )
        console.print(layout)
