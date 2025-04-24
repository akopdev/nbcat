from pathlib import Path

import pytest
from responses import RequestsMock

from nbcat.exceptions import InvalidNotebookFormatError, NotebookNotFoundError
from nbcat.main import read_notebook


@pytest.fixture
def path_to_assets() -> Path:
    return Path(__file__).parent / "assets/"


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("many_tracebacks.ipynb", 1),
        ("test3.ipynb", 9),
        ("test3_no_metadata.ipynb", 9),
        ("test3_no_min_version.ipynb", 0),
        ("test3_no_worksheets.ipynb", 0),
        ("test3_worksheet_with_no_cells.ipynb", 0),
        ("test4.5.ipynb", 9),
        ("test4.ipynb", 9),
        ("test4custom.ipynb", 2),
        ("test4docinfo.ipynb", 9),
        ("test4jupyter_metadata.ipynb", 1),
        ("test4jupyter_metadata_timings.ipynb", 2),
    ],
)
def test_read_local_notebook(filename: str, expected: int, path_to_assets: Path):
    nb = read_notebook(str(path_to_assets / filename))
    assert len(nb.cells) == expected


@pytest.mark.parametrize(
    "url,expected",
    [
        ("http://example.com/remote-notebook.ipynb", 2),
        ("https://example.com/remote-notebook.ipynb", 2),
    ],
)
def test_read_remote_notebook(
    url: str, expected: int, responses: RequestsMock, path_to_assets: Path
):
    responses.get(
        url,
        body=(path_to_assets / "test4custom.ipynb").read_text(encoding="utf-8"),
        status=200,
        content_type="application/json",
    )
    nb = read_notebook(url)
    assert len(nb.cells) == expected


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("not-exists-file.ipynb", NotebookNotFoundError),
        ("invalid.ipynb", InvalidNotebookFormatError),
    ],
)
def test_read_invalid_notebook(filename: str, expected: Exception, path_to_assets: Path):
    with pytest.raises(expected):
        read_notebook(str(path_to_assets / filename))
