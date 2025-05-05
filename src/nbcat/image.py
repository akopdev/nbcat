import base64
import shutil
from io import BytesIO
from platform import system

from PIL import Image as PilImage
from rich.console import Console, ConsoleOptions, RenderResult
from rich.text import Text
from timg import METHODS, Renderer


class Image:
    def __init__(self, image: str):
        img = BytesIO(base64.b64decode(image.replace("\n", "")))
        self.image = PilImage.open(img)

    @property
    def method_class(self):
        # TODO: auto detect terminal to benefit from sixel protocol support
        method = "a24h" if system() != "Windows" else "ascii"
        return METHODS[method]["class"]

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        img = Renderer()
        img.load_image(self.image)
        img.resize(shutil.get_terminal_size()[0] - 1)
        output = img.to_string(self.method_class)
        yield Text.from_ansi(output)
