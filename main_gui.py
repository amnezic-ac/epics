# This file will contain what the main user will launch when using the software with GUI
# for integration, please refer to ./main_api.py

import json
import tkinter as tk

from src.gui.gui_components import *

def importConfigFromJSONFile(filepath: str) -> dict:
    data = None
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

configuration = importConfigFromJSONFile("default_config.json")

main_window = tk.Tk()
main_window.title("ICS generator")

testFrame, eventObject = makeEventFrame(main_window, configuration)
testFrame.pack()

def exportConfigToJSONFile(filepath: str) -> bool:
    with open(filepath, "w", encoding='utf-8') as file:
        json.dump(configuration, file, indent=4)

main_window.mainloop()

exportConfigToJSONFile("default_config.json")
