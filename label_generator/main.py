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


class Label:
    epd = epd2in13d.EPD()
    FONT_SIZE = 24
    LINE_LENGTH = 18
    PAGE_SIZE = 72
    THRESHOLD = 125

    def __init__(self):
        self.epd.init()
        self.epd.Clear()

    def create_empty_frame(self, size):
        buffer = Image.new(
            "1", (self.epd.height, self.epd.width), 255
        )  # 255: clear the frame
        draw = ImageDraw.Draw(buffer)
        draw.rectangle([(0, 0), (size.width, size.height)], outline=0)
        return MonImage(dessin=draw, buffer=buffer)

    def get_size(self):
        return Size(width=self.epd.height, height=self.epd.width)

    def split_joke(self, joke_sentence):
        aggregation = [""]
        page_index = 0
        for part in joke_sentence.split():
            concat = f"{aggregation[page_index]} {part}"
            if len(concat) > self.PAGE_SIZE:
                page_index += 1
                aggregation.append("")
            aggregation[page_index] = aggregation[page_index] + " " + part
        return aggregation

    def print_joke(self, sentence: str):
        font = ImageFont.truetype("./Font.ttc", self.FONT_SIZE)
        size = self.get_size()
        image = self.create_empty_frame(size)

        lines = textwrap.wrap(sentence, width=self.LINE_LENGTH)
        for line_num, line in enumerate(lines):
            image.dessin.text(
                (5, 5 + line_num * self.FONT_SIZE), line, font=font, fill=0
            )

        self.epd.display(self.epd.getbuffer(image.buffer))

    def print_avatar(self, name):
        image_path = f"./avatars/{name}.bmp"
        buffer = Image.new(
            "1", (self.epd.height, self.epd.width), 255
        )  # 255: clear the frame
        fond = ImageDraw.Draw(buffer)
        size = self.get_size()
        fond.rectangle([(0, 0), (size.width, size.height)], outline=0)
        font = ImageFont.truetype("./Font.ttc", self.FONT_SIZE)
        buffer.paste(Image.open(image_path), (0, 0))
        fond.text((114, (104 / 2) - (self.FONT_SIZE / 2)), name, font=font, fill=0)
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
    Label().print_avatar("Denis")
