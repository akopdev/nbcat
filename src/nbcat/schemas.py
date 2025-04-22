from typing import Any
from pydantic import BaseModel, Field, computed_field

from .enums import CellType, OutputType


class BaseOutput(BaseModel):
    output_type: OutputType
    execution_count: int | None = None


class StreamOutput(BaseOutput):
    name: str
    text: list[str] | str

    @computed_field
    @property
    def output(self) -> str:
        if isinstance(self.text, list):
            return "".join(self.text)
        return self.text


class DisplayDataOutput(BaseOutput):
    data: dict[str, Any]

    @computed_field
    @property
    def output(self) -> str:
        # TODO: add support for rich display outputs
        return ""


class ErrorOutput(BaseOutput):
    ename: str
    evalue: str
    traceback: list[str]

    @computed_field
    @property
    def output(self) -> str:
        return "\n".join(self.traceback)


class Cell(BaseModel):
    cell_type: CellType
    source: list[str] | str
    execution_count: int | None = None
    outputs: list[StreamOutput | DisplayDataOutput | ErrorOutput] = []

    @computed_field
    @property
    def input(self) -> str:
        if isinstance(self.source, list):
            return "".join(self.source)
        return self.source


class Notebook(BaseModel):
    cells: list[Cell]
