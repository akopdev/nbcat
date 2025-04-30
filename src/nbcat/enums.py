from enum import Enum


class CellType(str, Enum):
    MARKDOWN = "markdown"
    CODE = "code"
    RAW = "raw"
    HEADING = "heading"


class OutputType(str, Enum):
    STREAM = "stream"
    DISPLAY_DATA = "display_data"
    EXECUTE_RESULT = "execute_result"
    ERROR = "error"
    PYOUT = "pyout"


class OutputCellType(str, Enum):
    PLAIN = "plain"
    HTML = "html"
    IMAGE = "image"
    JSON = "json"
