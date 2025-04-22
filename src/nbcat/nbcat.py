import os
import urllib.request
from pathlib import Path

from pydantic import AnyHttpUrl, ValidationError

from nbcat.schemas import Notebook

from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.console import Console


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

    def read(self, source: str | AnyHttpUrl):
        if isinstance(source, AnyHttpUrl):
            with urllib.request.urlopen(str(source)) as response:
                content = response.read().decode("utf-8")
        else:
            content = Path(source).read_text(encoding="utf-8")
        return Notebook.model_validate_json(content)

    def print(self):
        nb = self.read(self.file)
        console = Console()
        for cell in nb.cells:
            if cell.cell_type == "markdown":
                stdout = Markdown("".join(cell.source))
            elif cell.cell_type == "code":
                stdout = Panel(Syntax("".join(cell.source), "python", theme=self.theme))
            console.print(stdout)
