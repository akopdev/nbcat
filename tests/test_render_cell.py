from rich.console import Group

from nbcat.main import render_cell
from nbcat.schemas import Cell, StreamOutput


def test_render_cell_with_outputs():
    output_1 = StreamOutput(text=["First output"], execution_count=7, output_type="stream")
    output_2 = StreamOutput(text=["Second output"], output_type="stream")

    cell = Cell(
        cell_type="code",
        source="print('Hello')",
        execution_count=None,
        outputs=[output_1, output_2],
    )

    rendered = render_cell(cell)

    assert isinstance(rendered, Group)
    assert len(rendered.renderables) == 3


def test_render_cell_skips_empty_outputs():
    output = StreamOutput(text="", execution_count=99, output_type="stream")
    cell = Cell(
        cell_type="raw",
        source="Raw input",
        execution_count=1,
        outputs=[output],
    )

    rendered = render_cell(cell)

    assert isinstance(rendered, Group)
