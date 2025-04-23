class InvalidNotebookFormatError(Exception):
    """Raised when the file is not a valid .ipynb or URL."""


class NotebookNotFoundError(Exception):
    """Raised when the file or URL is not reachable."""


class UnsupportedNotebookTypeError(Exception):
    """Raised when the file exists but is not a .ipynb document."""
