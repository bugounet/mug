import os
from random import randrange

api_key = os.environ.get("AIRTABLE_API_KEY", None)

from pyairtable import Table

base_id = "app60r3wYfbygIeZ5"
table_name = "tblVGZBO6BSTH1EHL"

table = Table(api_key, base_id, table_name)

jokes = []
jokes_table_data = table.all()

for jokes_table_data_item in jokes_table_data:
    jokes.append(jokes_table_data_item.get("fields").get("Blague"))

import time, threading

StartTime = time.time()

last_joke_index = None


def print_next_joke():
    global last_joke_index
    random_joke_index = randrange(len(jokes))
    while random_joke_index == last_joke_index:
        random_joke_index = randrange(len(jokes))

    last_joke_index = random_joke_index
    random_joke = jokes[random_joke_index]
    print_joke(random_joke)


class setInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time() + self.interval
        while not self.stopEvent.wait(nextTime - time.time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()


JOKES_SELECTION_INTERVAL = int(os.environ.get("JOKES_SELECTION_INTERVAL", 5)) or 10
inter = setInterval(JOKES_SELECTION_INTERVAL, print_next_joke)


from label_generator.main import Label

label = Label()


def print_joke(sentence: str):
    print(" got joke:", sentence)
    if sentence:
        pages = label.split_joke(sentence)
        for page in pages:
            label.print_joke(page)
            if len(pages):
                print("wait 5s")
                time.sleep(5)
