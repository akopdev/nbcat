import shutil
from io import BytesIO

from PIL import Image as PilImage
from textual_image.renderable import Image
from textual_image.renderable.halfcell import Image as HalfcellImage
from textual_image.renderable.sixel import Image as SixelImage
from textual_image.renderable.tgp import Image as TGPImage
from textual_image.renderable.unicode import Image as UnicodeImage


def render_image(image_content: bytes) -> TGPImage | SixelImage | HalfcellImage | UnicodeImage:
    """
    Render an image from raw byte content and adjusts it to fit the terminal width.

    Args:
        image_content (bytes): The raw byte content of the image.

    Returns
    -------
        TGPImage | SixelImage | HalfcellImage | UnicodeImage: A terminal-compatible image
        object adjusted to the current terminal width.
    """
    image = PilImage.open(BytesIO(image_content))
    width = min(image.size[0], shutil.get_terminal_size()[0])
    return Image(image, width=width, height="auto")
