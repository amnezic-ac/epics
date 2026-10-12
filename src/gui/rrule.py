from tkinter import ttk
import tkinter as tk
import tkcalendar as tkc
from datetime import datetime
from src.utils import configuration

def makeByXxxFrame(root: tk.Frame, xxx: str) -> tk.Listbox :
    xxxList = [
        "sec",
        "minute",
        "hour",
        "day",
        "monthday",
        "yearday",
        "weekno",
        "month",
        "setpos"
    ]
    if (not xxx in xxxList):
        raise Exception(f"by{xxx} is not a valid byXxx list")

    frame = ttk.Frame(root)
    listbox = tk.Listbox(
        frame,
        selectmode="multiple",
        height=configuration["rrule"][f"{xxx}"]["height"],
        exportselection=False,
    )
    for i in range (len(configuration["rrule"][f"{xxx}"]["choices"])):
        listbox.insert(i, configuration["rrule"][f"{xxx}"]["choices"][i])
    listbox.pack(side="left")
    ttk.Label(frame, text=configuration["rrule"][f"{xxx}"]["label"]).pack(side="right")
    frame.pack()
    return listbox

