# This file will contain what the main user will launch when using the software with GUI
# for integration, please refer to ./main_api.py

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

from src.gui.components import event, calendar
from src.utils import configuration, exportConfigToJSONFile, logging

from src.gui.properties import makeRruleFrame


logging.debug(f"New session activated")

root = tk.Tk()
root.rowconfigure(1, weight=1)
root.columnconfigure(1, weight=1)

frame, _ = makeRruleFrame(root)
frame.grid(row=1, column=1, sticky=tk.NSEW)

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
def createNewCalendar(master):
    logging.debug(f"User tries to create a new calendar")
    frame, _ = calendar.create(master)

def createEvent(masterFrame):
    eventFrame, eventDict = event.makeEventFrame(masterFrame)

filemenu.add_command(label="Create", command=lambda : createNewCalendar(root))
filemenu.add_command(label="Export", command=lambda: logging.debug(f"User clicked on calendar export"))
filemenu.add_command(label="Import", command=lambda: logging.debug(f"User clicked on calendar import"))
filemenu.add_command(label="Remove", command=lambda: logging.debug(f"User clicked on calendar removal"))
menubar.add_cascade(label="Calendar", menu=filemenu)

# file = None
# text = tk.Text(root, height=12)
# def getICSFile():
#     file = fd.askopenfile()
#     print(text.insert('1.0', file.readlines()))
# 
# calendarChoiceButton = tk.Button(root, text="Choose a calendar", command = getICSFile)
# calendarChoiceButton.pack()

root.config(menu=menubar)
root.mainloop()

exportConfigToJSONFile("default_config.json")
logging.debug(f"Session ended")
