from pathlib import Path

import pytest

from nbcat.exceptions import InvalidNotebookFormatError, NotebookNotFoundError
from nbcat.main import read_notebook


@pytest.fixture
def path_to_assets() -> Path:
    return Path(__file__).parent / "assets/"


@pytest.mark.parametrize(
    "filename",
    [
        ("many_tracebacks.ipynb",),
        ("test3.ipynb",),
        ("test3_no_metadata.ipynb",),
        ("test3_no_min_version.ipynb",),
        ("test3_no_worksheets.ipynb",),
        ("test3_worksheet_with_no_cells.ipynb",),
        ("test4.5.ipynb",),
        ("test4.ipynb",),
        ("test4custom.ipynb",),
        ("test4docinfo.ipynb",),
        ("test4jupyter_metadata.ipynb",),
        ("test4jupyter_metadata_timings.ipynb",),
    ],
)
def test_local_read_notebook(filename: str, path_to_assets: Path):
    print(str(path_to_assets / filename[0]))
    assert read_notebook(str(path_to_assets / filename[0]))


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("not-exists-file.ipynb", NotebookNotFoundError),
        ("invalid.ipynb", InvalidNotebookFormatError),
    ],
)
def test_read_notebook_invalid_json_raises(
    filename: str, expected: Exception, path_to_assets: Path
):
    with pytest.raises(expected):
        read_notebook(str(path_to_assets / filename))
