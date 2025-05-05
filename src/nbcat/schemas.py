from typing import Any, Union

from pydantic import BaseModel, computed_field, model_validator

from .enums import CellType, OutputCellType, OutputType
from .exceptions import InvalidNotebookFormatError


class BaseOutput(BaseModel):
    output_type: OutputType
    execution_count: Union[int, None] = None


class CellOutput(BaseModel):
    output_type: OutputCellType
    text: str


class StreamOutput(BaseOutput):
    text: Union[list[str], str]

    @computed_field
    @property
    def output(self) -> CellOutput:
        text = "".join(self.text) if isinstance(self.text, list) else self.text
        return CellOutput(output_type=OutputCellType.PLAIN, text=text)


class DisplayDataOutput(BaseOutput):
    data: dict[str, Any]

    @computed_field
    @property
    def output(self) -> Union[CellOutput, None]:
        data_type_map = {
            "text/html": OutputCellType.HTML,
            "image/png": OutputCellType.IMAGE,
            "text/plain": OutputCellType.PLAIN,
            "application/vnd.raw.v1+json": OutputCellType.JSON,
        }
        for data_type, output_type in data_type_map.items():
            data = self.data.get(data_type)
            if data:
                text = "".join(data) if isinstance(data, list) else str(data)
                return CellOutput(output_type=output_type, text=text)


class ErrorOutput(BaseOutput):
    ename: str
    evalue: str
    traceback: list[str]

    @computed_field
    @property
    def output(self) -> CellOutput:
        return CellOutput(output_type=OutputCellType.PLAIN, text="\n".join(self.traceback))


class PyoutDataOutput(BaseOutput):
    text: list[str]

    @computed_field
    @property
    def output(self) -> CellOutput:
        return CellOutput(output_type=OutputCellType.PLAIN, text="\n".join(self.text))


class Cell(BaseModel):
    cell_type: CellType
    source: Union[list[str], str]
    level: Union[int, None] = None
    execution_count: Union[int, None] = None
    outputs: list[Union[StreamOutput, DisplayDataOutput, ErrorOutput, PyoutDataOutput]] = []

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
