from typing import Any
from pydantic import BaseModel, Field

from .enums import CellType, OutputType

class MetadataJupyter(BaseModel):
    source_hidden: bool = False
    outputs_hidden: bool = False

class Metadata(BaseModel):
    jupyter: MetadataJupyter | None = Field(default_factory=MetadataJupyter)


class BaseOutput(BaseModel):
    output_type: OutputType

class StreamOutput(BaseOutput):
    name: str
    text: list[str] | None = []

class DisplayDataOutput(BaseOutput):
    data: dict[str, Any]

class ErrorOutput(BaseOutput):
    ename: str
    evalue: str
    traceback: list[str]


class Cell(BaseModel):
    cell_type: CellType
    id: str
    source: list[str]
    metadata: Metadata
    execution_count: int | None = None
    outputs: list[StreamOutput | DisplayDataOutput | ErrorOutput] = []

class Notebook(BaseModel):
    cells: list[Cell]
