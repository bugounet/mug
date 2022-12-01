from waveshare_epd import epd2in13d
from dataclasses import dataclass
import time
from PIL import Image, ImageDraw, ImageFont
from typing import Any

joke = (
    "Je ne dis pas que je suis Batman. "
    "Je dis juste qu'on ne nous a jamais vu ensembles dans la même pièce."
)
import textwrap


@dataclass
class Size:
    width: int
    height: int


@dataclass
class MonImage:
    dessin: Any
    buffer: Any


def create_empty_frame(size):
    buffer = Image.new("1", (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(buffer)
    draw.rectangle([(0, 0), (size.width, size.height)], outline=0)
    return MonImage(dessin=draw, buffer=buffer)


def get_size(epd):
    return Size(width=epd.height, height=epd.width)


epd = epd2in13d.EPD()

FONT_SIZE = 15
line_LENGTH = 28


def print_joke(sentence: str):
    epd.init()
    epd.Clear()

    font = ImageFont.truetype("./Font.ttc", FONT_SIZE)
    size = get_size(epd)
    image = create_empty_frame(size)

    lines = textwrap.wrap(sentence, width=28)
    for line_num, line in enumerate(lines):
        image.dessin.text((5, 5 + line_num * FONT_SIZE), line, font=font, fill=0)

    epd.display(epd.getbuffer(image.buffer))


if __name__ == "__main__":
    print_joke(joke)
