import discord
import aiohttp
import io

from PIL import Image, ImageFilter
from typing import Union

from colorthief import ColorThief


async def get_image_from_url(url: str, size: tuple = None) -> Image.Image:
    """Get image from url and resize it if size is specified.

    Args:
        url (str): Image url.
        size (tuple, optional): Size to resize image to. Defaults to None.

    Returns:
        Image.Image: Image object.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            img = Image.open(io.BytesIO(await resp.read()))

    return img.resize(size, Image.ANTIALIAS) if size else img


async def get_most_freq_colour(img: Union[str, Image.Image]) -> discord.Colour:
    """Get most frequent colour from image.

    Args:
        img (Union[str, Image.Image]): Image url or Image object.

    Returns:
        discord.Colour: Most frequent colour.
    """
    if isinstance(img, str):
        img = await get_image_from_url(img)

    img = img.convert("RGB").filter(ImageFilter.GaussianBlur(100))

    img_bytes = io.BytesIO()
    img.save(img_bytes, "png")

    rgb = ColorThief(img_bytes).get_palette(5, 5)[0]
    return discord.Colour.from_rgb(*rgb)
