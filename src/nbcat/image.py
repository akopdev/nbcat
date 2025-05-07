import base64
import shutil
from io import BytesIO
from platform import system

from PIL import Image as PilImage
from rich.console import Console, ConsoleOptions, RenderResult
from rich.text import Text
from timg import METHODS, Renderer


class Image:
    def __init__(self, image: str, method: str = "a24h"):
        img = BytesIO(base64.b64decode(image.replace("\n", "")))
        self.image = PilImage.open(img)
        self.method = method if system() != "Windows" else "ascii"

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        renderer = Renderer()
        renderer.load_image(self.image)
        width = shutil.get_terminal_size()[0] - 1
        if self.method == "sixel":
            width = width * 6

        renderer.resize(width)

        if self.method == "sixel":
            renderer.reduce_colors(16)

        output = renderer.to_string(METHODS[self.method]["class"])
        yield Text.from_ansi(output, no_wrap=True, end="")
