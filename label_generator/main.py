from waveshare_epd import epd2in13d
from dataclasses import dataclass
import time
from PIL import Image, ImageDraw, ImageFont
from typing import Any
import textwrap
import time


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


class Label:
    epd = epd2in13d.EPD()
    FONT_SIZE = 24
    LINE_LENGTH = 18
    PAGE_SIZE = 72
    THRESHOLD = 125

    def __init__(self):
        self.epd.init()
        self.epd.Clear()

    def split_joke(self, joke_sentence):
        aggregation = [""]
        page_index = 0
        for part in joke_sentence.split():
            concat = f"{aggregation[page_index]} {part}"
            if len(concat) > PAGE_SIZE:
                page_index += 1
                aggregation.append("")
            aggregation[page_index] = aggregation[page_index] + " " + part
        return aggregation

    def print_joke(self, sentence: str):
        font = ImageFont.truetype("./Font.ttc", FONT_SIZE)
        size = get_size(epd)
        image = create_empty_frame(size)

        lines = textwrap.wrap(sentence, width=LINE_LENGTH)
        for line_num, line in enumerate(lines):
            image.dessin.text((5, 5 + line_num * FONT_SIZE), line, font=font, fill=0)

        epd.display(epd.getbuffer(image.buffer))

    def print_image(self, image_path):
        buffer = Image.open(image_path)

        buffer = buffer.convert("L")
        # Threshold
        buffer = buffer.point(lambda p: 255 if p > self.THRESHOLD else 0)
        # To mono
        buffer = buffer.convert("1")
        self.epd.display(self.epd.getbuffer(buffer))


if __name__ == "__main__":
    # joke = (
    #     "Je ne dis pas que je suis Batman. "
    #     "Je dis juste qu'on ne nous a jamais vu ensembles dans la même pièce."
    # )
    # pages = split_joke(joke)
    # for page in pages:
    #     print_joke(page)
    #     time.sleep(5)
    Label().print_image(image_path="./avatars/Jordane.jpeg")
