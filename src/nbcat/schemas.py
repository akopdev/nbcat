from typing import Literal

from pydantic import BaseModel


class OutputStream(BaseModel):
    output_type: Literal["stream"]
    name: str
    text: list[str]


class CodeCell(BaseModel):
    cell_type: Literal["code"]
    id: str
    source: list[str]
    execution_count: int | None
    outputs: list[OutputStream]


class MarkdownCell(BaseModel):
    cell_type: Literal["markdown"]
    id: str
    source: list[str]


class Notebook(BaseModel):
    cells: list[CodeCell | MarkdownCell]
