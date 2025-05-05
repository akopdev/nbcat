# In an ideal world, this code shouldn't exist. However, for reasons unknown to me,
# `rich` decided to format markdown headers in a way that makes them unusable
# in the terminal: they are centered and wrapped in a Panel, which causes them to
# blend in with the rest of the content. It takes me time to understand what I'm
# looking at.
#
# Instead, I override the default implementation by adding colors and preserving
# the original formatting, so that the headers remain recognizable even on
# black-and-white screens.

from __future__ import annotations

from typing import ClassVar

from rich import markdown as md
from rich.console import Console, ConsoleOptions, RenderResult
from rich.text import Text


class Heading(md.Heading):
    """A heading."""

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        styles = {
            "h1": "bold cyan",
            "h2": "bold magenta",
            "h3": "bold yellow",
        }
        indent = int(self.tag.strip("h"))
        yield Text(f"{'#' * indent} {self.text}", style=styles.get(self.tag, "dim white"))


class Markdown(md.Markdown):
    elements: ClassVar[dict[str, type[md.MarkdownElement]]] = {
        "paragraph_open": md.Paragraph,
        "heading_open": Heading,
        "fence": md.CodeBlock,
        "code_block": md.CodeBlock,
        "blockquote_open": md.BlockQuote,
        "hr": md.HorizontalRule,
        "bullet_list_open": md.ListElement,
        "ordered_list_open": md.ListElement,
        "list_item_open": md.ListItem,
        "image": md.ImageItem,
        "table_open": md.TableElement,
        "tbody_open": md.TableBodyElement,
        "thead_open": md.TableHeaderElement,
        "tr_open": md.TableRowElement,
        "td_open": md.TableDataElement,
        "th_open": md.TableDataElement,
    }
