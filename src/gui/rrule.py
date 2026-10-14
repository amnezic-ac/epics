from tkinter import ttk
import tkinter as tk
import tkcalendar as tkc
from datetime import datetime
from src.utils import configuration

def makeByXxxFrame(root: tk.Frame, userChoice: str) -> tk.Listbox :
    xxx = ""
    match userChoice:
        case "day number of the month":
            xxx = "monthday"
        case "day number of the year":
            xxx = "yearday"
        case "week number of the year":
            xxx = "yearday"
        case "month number of the year":
            xxx = "month"
        case "hour"|"minute"|"second":
            raise Exception(f"{userChoice} hasn't been implement yet")
        case _:
            raise Exception(f"Invalid user choice")
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
    config = configuration["rrule"][f"{xxx}"]
    choices = []
    if (xxx in ["month", "day"]):
        choices = config["choices"]
    else:
        choices = [i for i in range (config["min"], config["max"]+1, config["step"])]

    listbox = tk.Listbox(frame, listvariable=tk.Variable(value=choices), height=5)

    # spinbox = ttk.Spinbox(
    #     frame,
    #     exportselection=False,
    #     justify=tk.RIGHT,
    # )
    # if (xxx in ["month", "day"]):
    #     spinbox.config(
    #         values=configuration["rrule"][f"{xxx}"]["choices"]
    #     )
    # else:
    #     spinbox.config(
    #         from_=configuration["rrule"][f"{xxx}"]["min"],
    #         to=configuration["rrule"][f"{xxx}"]["max"],
    #         increment=configuration["rrule"][f"{xxx}"]["step"],
    #         wrap=True,
    #         width = 4,
    #     )
    # spinbox.pack(side="left")
    listbox.pack(side="left")
    ttk.Label(frame, text=configuration["rrule"][f"{xxx}"]["label"]).pack(side="right")

    result = {
        "frame": frame,
        "xxx": xxx,
        "spinbox": listbox
    }

    return result

def makeRuleFrame(root: tk.Frame, freq: str, removable: bool = True, remaining: int = 0):
    frame = ttk.Frame(root)
    frame.rowconfigure(1)
    for i in range (5):
        frame.columnconfigure(i, weight=1)
    ttk.Label(frame, text="Rule: ").grid(row=0, column=0, sticky=tk.W)

    choices = None
    match freq:
        case "yearly":
            choices = ["day number of the month", "day number of the year", "week number of the year", "month number of the year"]
        case _:
            raise Exception(f"{freq} is not a valid frequence")
    combobox = ttk.Combobox(
        frame,
        values=choices,
        exportselection=False
    )
    combobox.grid(row=0, column=1, sticky=tk.W)

    def makeXxxFrame(event):
        selected_value = event.widget.get()
        truc = makeByXxxFrame(frame, selected_value)
        truc["frame"].grid(row=0, column=2)

    combobox.bind("<<ComboboxSelected>>", makeXxxFrame)

    def foo():
        fooFrame = makeRuleFrame(root, freq)
        fooFrame.pack(fill="x")

    if (removable):
        ttk.Button(frame, text="-", command=frame.destroy).grid(row=0, column=3, sticky=tk.E)
        ttk.Button(frame, text="+", command=foo).grid(row=0, column=4, sticky=tk.E)
    else:
        ttk.Button(frame, text="+", command=foo).grid(row=0, column=3, columnspan=2, sticky=tk.E)
    return frame


def makeYearlyFrame(root: tk.Frame) -> (tk.Frame, dict):
    frame = ttk.Frame(root)

    ruleFrame = makeRuleFrame(frame, "yearly", False)
    ruleFrame.pack(fil="x")

    valueHolder = {
        "byday": None,
        "bymonthday": None,
    }

    return frame, None