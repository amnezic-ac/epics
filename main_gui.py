# This file will contain what the main user will launch when using the software with GUI
# for integration, please refer to ./main_api.py

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

from src.gui.gui_components import *
from utils import configuration, exportConfigToJSONFile, logging


logging.debug(f"New session activated")

root = tk.Tk()

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
def createEvent(masterFrame):
    eventFrame, eventDict = makeEventFrame(masterFrame)

filemenu.add_command(label="New event", command=lambda: createEvent(root))
filemenu.add_command(label="New task", command=lambda: logging.debug("New task frame opened"))
filemenu.add_command(label="New alarm", command=lambda: logging.debug("New alaram opened"))
filemenu.add_command(label="New journal", command=lambda: logging.debug("New journal frame opened"))
menubar.add_cascade(label="Calendar", menu=filemenu)

file = None
text = tk.Text(root, height=12)
def getICSFile():
    file = fd.askopenfile()
    print(text.insert('1.0', file.readlines()))

calendarChoiceButton = tk.Button(root, text="Choose a calendar", command = getICSFile)
calendarChoiceButton.pack()

root.config(menu=menubar)
root.mainloop()

exportConfigToJSONFile("default_config.json")
logging.debug(f"Session ended")
