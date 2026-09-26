from tkinter import *
from tkcalendar import Calendar, DateEntry
from datetime import datetime

import json
from gui_property import *

def importConfigFromJSONFile(filepath: str) -> dict:
    data = None
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

configuration = importConfigFromJSONFile("default_config.json")

main_window = Tk()
main_window.title("ICS generator")

test_frame = make_prioriity_frame(main_window, configuration)
test_frame.pack()

def exportConfigToJSONFile(filepath: str) -> bool:
    with open(filepath, "w", encoding='utf-8') as file:
        json.dump(configuration, file, indent=4)

main_window.mainloop()

exportConfigToJSONFile("default_config.json")