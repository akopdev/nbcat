from typing import Any

from pydantic import BaseModel, computed_field, model_validator

from .enums import CellType, OutputType
from .exceptions import InvalidNotebookFormatError


class BaseOutput(BaseModel):
    output_type: OutputType
    execution_count: int | None = None


class StreamOutput(BaseOutput):
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


class PyoutDataOutput(BaseOutput):
    text: list[str]

    @computed_field
    @property
    def output(self) -> str:
        return "\n".join(self.text)


class Cell(BaseModel):
    cell_type: CellType
    source: list[str] | str
    level: int | None = None
    execution_count: int | None = None
    outputs: list[StreamOutput | DisplayDataOutput | ErrorOutput | PyoutDataOutput] = []

    @model_validator(mode="before")
    @classmethod
    def handle_format_versions(cls, data: dict[str, Any]) -> dict[str, Any]:
        if data.get("input"):
            data["source"] = data["input"]
        return data

    @computed_field
    @property
    def input(self) -> str:
        if self.cell_type == CellType.HEADING and self.level is not None:
            return f"{'#' * self.level} {''.join(self.source)}"

        if isinstance(self.source, list):
            return "".join(self.source)

        return self.source


class Notebook(BaseModel):
    cells: list[Cell] = []
    nbformat: int

    @model_validator(mode="before")
    @classmethod
    def handle_format_versions(cls, data: dict[str, Any]) -> dict[str, Any]:
        if data.get("worksheets"):
            try:
                data["cells"] = data.get("worksheets", [{"cells": []}])[0].get("cells", [])
            except (KeyError, IndexError, TypeError) as e:
                print(e)
                raise InvalidNotebookFormatError(f"Invalid v3 notebook structure: {e}")
        return data
