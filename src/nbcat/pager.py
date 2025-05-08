from rich.console import RenderableType
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.widgets import Static


class Pager(App):
    BINDINGS = [
        # Exit
        Binding("q", "quit", "Quit"),
        Binding(":q", "quit", "Quit"),
        Binding("Q", "quit", "Quit"),
        Binding(":Q", "quit", "Quit"),
        Binding("ZZ", "quit", "Quit"),
        # One line
        Binding("j", "scroll_down", "Down"),
        Binding("e", "scroll_down", "Down"),
        Binding("^e", "scroll_down", "Down"),
        Binding("^n", "scroll_down", "Down"),
        Binding("cr", "scroll_down", "Down"),  # carriage return = Enter
        Binding("k", "scroll_up", "Up"),
        Binding("y", "scroll_up", "Up"),
        Binding("ctrl+y", "scroll_up", "Up"),
        Binding("ctrl+k", "scroll_up", "Up"),
        Binding("ctrl+p", "scroll_up", "Up"),
        # One window
        Binding("f", "page_down", "Page Down"),
        Binding("ctrl+f", "page_down", "Page Down"),
        Binding("ctrl+v", "page_down", "Page Down"),
        Binding("space", "page_down", "Page Down"),
        Binding("b", "page_up", "Page Up"),
        Binding("ctrl+b", "page_up", "Page Up"),
        Binding("escape+v", "page_up", "Page Up"),
        # Extended window control
        Binding("z", "page_down", "Window Down (set N)"),
        Binding("w", "page_up", "Window Up (set N)"),
        Binding("escape+space", "page_down", "Forward one window, no EOF stop"),
        Binding("d", "half_page_down", "Half Page Down"),
        Binding("ctrl+d", "half_page_down", "Half Page Down"),
        # Jumping
        Binding("g", "go_to_top", "Top of File"),
        Binding("<", "go_to_top", "Top of File"),
        Binding("escape+<", "go_to_top", "Top of File"),
        Binding("G", "go_to_bottom", "Bottom of File"),
        Binding(">", "go_to_bottom", "Bottom of File"),
        Binding("escape+>", "go_to_bottom", "Bottom of File"),
    ]

    def __init__(self, objects: list[RenderableType]):
        super().__init__()
        self._objects = objects

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            for obj in self._objects:
                yield Static(obj)

    def on_mount(self) -> None:
        self.theme = "textual-ansi"
        self.viewer = self.query_one(VerticalScroll)

    def action_scroll_down(self) -> None:
        self.viewer.scroll_to(y=self.viewer.scroll_y + 1)

    def action_scroll_up(self) -> None:
        self.viewer.scroll_to(y=self.viewer.scroll_y - 1)

    def action_page_down(self) -> None:
        self.viewer.scroll_to(y=self.viewer.scroll_y + self.viewer.virtual_size.height)

    def action_page_up(self) -> None:
        self.viewer.scroll_to(y=max(self.viewer.scroll_y - self.viewer.virtual_size.height, 0))

    def action_half_page_down(self) -> None:
        self.viewer.scroll_to(y=self.viewer.scroll_y + (self.viewer.virtual_size.height / 2))

    def action_go_to_top(self) -> None:
        self.viewer.scroll_to(y=0)

    def action_go_to_bottom(self) -> None:
        self.viewer.scroll_to(y=self.viewer.virtual_size.height)
