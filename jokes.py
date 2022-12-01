import enum
from datetime import datetime
import os
from random import randrange

api_key = os.environ.get("AIRTABLE_API_KEY", None)

from pyairtable import Table

base_id = 'app60r3wYfbygIeZ5'
jokes_table_name = 'tblVGZBO6BSTH1EHL'
stage_table_name = 'tbled2cqBrnQlMzrw'

jokes_table = Table(api_key, base_id, jokes_table_name)

jokes = []
jokes_table_data = jokes_table.all()

for jokes_table_data_item in jokes_table_data:
    jokes.append(jokes_table_data_item.get("fields").get("Blague"))

import time

last_joke_index = None
joke_display_started_at = None

JOKES_SELECTION_INTERVAL = int(os.environ.get("JOKES_SELECTION_INTERVAL", None)) or 10

def joke_display_time_expired(start_time: datetime):
    return int((datetime.now() - start_time).total_seconds()) >= JOKES_SELECTION_INTERVAL

last_joke_index = None
def pick_next_joke():
    global last_joke_index

    random_joke_index = randrange(len(jokes))    
    while random_joke_index == last_joke_index:
        random_joke_index = randrange(len(jokes))

    last_joke_index = random_joke_index
    next_joke = jokes[random_joke_index]

    return next_joke

def display_joke() :
    global joke_display_started_at
    
    if not last_joke_index or not joke_display_started_at or joke_display_time_expired(start_time=joke_display_started_at):
        joke_display_started_at = datetime.now()
        next_joke = pick_next_joke()        
        print_joke(next_joke)


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

class AppStage(enum.Enum):
    DISPLAY_QR_CODE = "DISPLAY_QR_CODE"
    DISPLAY_JOKES = "DISPLAY_JOKES"

def get_current_app_stage() -> AppStage:
    current_stage_table = Table(api_key, base_id, stage_table_name)
    current_stage_table_data = current_stage_table.all()
    print(f"current_stage_table_data: {current_stage_table_data}")
    current_stage = current_stage_table_data[0].get("fields").get("Stage")

    if "joke" in current_stage.lower():
        return AppStage.DISPLAY_JOKES
    elif "qr" in current_stage.lower():
        return AppStage.DISPLAY_QR_CODE

QR_CODE_DISPLAYED = False
def display_qr_code():
    global QR_CODE_DISPLAYED
    if not QR_CODE_DISPLAYED:
        print("QR CODE")
        QR_CODE_DISPLAYED = True

def clear_display_qr_code_state():
    global QR_CODE_DISPLAYED
    QR_CODE_DISPLAYED = False

def clear_display_jokes_state():
    global last_joke_index
    global joke_display_started_at

    last_joke_index = None
    joke_display_started_at = None


if __name__ == "__main__":
    while True:
        current_app_stage = get_current_app_stage()
        if current_app_stage == AppStage.DISPLAY_QR_CODE:
            clear_display_jokes_state()
            display_qr_code()
        elif current_app_stage == AppStage.DISPLAY_JOKES:
            clear_display_qr_code_state()
            display_joke()
        
        time.sleep(1)
