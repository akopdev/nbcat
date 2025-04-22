from typing import Any
from pydantic import BaseModel, Field, computed_field

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
    text: list[str]

    @computed_field
    @property
    def output(self) -> str:
        return "".join(self.text)


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
    source: list[str]
    metadata: Metadata
    execution_count: int | None = None
    outputs: list[StreamOutput | DisplayDataOutput | ErrorOutput] = []

    @computed_field
    @property
    def input(self) -> str:
        return "".join(self.source)

    @computed_field
    @property
    def output(self) -> str:
        result = ""
        if self.outputs:
            for o in self.outputs:
                if o.output:
                    result += o.output
        return result


class Notebook(BaseModel):
    cells: list[Cell]
