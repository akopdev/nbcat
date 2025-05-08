from rich.console import RenderableType
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widgets import Footer, Static


class Viewer(App):
    BINDINGS = [
        Binding("j", "scroll_down", "Down"),
        Binding("k", "scroll_up", "Up"),
        Binding("q", "quit", "Quit"),
    ]

    key_sequence = reactive("")

    def __init__(self, objects: list[RenderableType]):
        super().__init__()
        self._objects = objects

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            for obj in self._objects:
                yield Static(obj)
            yield Footer()

    def on_mount(self) -> None:
        self.theme = "textual-ansi"
        self.viewer = self.query_one(VerticalScroll)

    def action_scroll_down(self) -> None:
        self.viewer.scroll_to(y=self.viewer.scroll_y + 1)

    def action_scroll_up(self) -> None:
        self.viewer.scroll_to(y=self.viewer.scroll_y - 1)
