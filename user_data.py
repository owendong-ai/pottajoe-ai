import json
import os

FILE_NAME = "preferences.json"

def load_preferences():
    if not os.path.exists(FILE_NAME):
        return {
            "濃郁": 0,
            "果香": 0,
            "堅果": 0,
            "花香": 0
        }

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except:
        return {
            "濃郁": 0,
            "果香": 0,
            "堅果": 0,
            "花香": 0
        }

def save_preferences(preferences):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(preferences, file, ensure_ascii=False, indent=4)