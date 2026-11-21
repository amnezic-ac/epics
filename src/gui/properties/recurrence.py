from src.gui.imports import *
from src.backend.properties.recurrence import Rrule

# TODO
def makeRruleFrame(root, time_included: bool = True):
    frame = ttk.Frame(root)
    rules = {
        "freq": None,
        "until": None,
        "count": None,
        "interval": None,
        "bysecond": None,
        "byminute": None,
        "byhour": None,
        "byday": None,
        "bymonthday": None,
        "byyyearday": None,
        "byweekno": None,
        "bymonth": None,
        "bysetpos": None,
        "wkst": None
    }


    mandatoryFrame = ttk.Frame(frame)
    for row in range (2):
        mandatoryFrame.rowconfigure(row, weight=1)
    for col in range (6):
        mandatoryFrame.columnconfigure(col, weight=1)
    tk.Label(mandatoryFrame, text="Frequency ").grid(row=0, column=0, sticky=tk.W)
    freqValue = tk.StringVar(value="")
    frequencyCombobox = ttk.Combobox(
        mandatoryFrame,
        values = ["yearly", "monthly", "weekly", "daily", "hourly", "minutely", "secondly"],
        state="readonly",
        textvariable=freqValue
    )
    frequencyCombobox.grid(row=0, column=1, sticky=tk.W)
    intervalValue = tk.IntVar(value=1)
    intervalSpinbox = ttk.Spinbox(
        mandatoryFrame,
        from_=1,
        to=configuration["rrule"]["interval"]["max"],
        wrap=True,
        textvariable=intervalValue,
        width=4
    )
    ttk.Label(mandatoryFrame, text="Interval").grid(row=1, column=0, sticky=tk.W)
    intervalSpinbox.grid(row=1, column=1, columnspan=5, sticky=tk.W)

    tk.Label(mandatoryFrame, text="Repeat ").grid(row=0, column=2, rowspan=2, columnspan=4, sticky=tk.NW)
    repeatCombobox = ttk.Combobox(
        mandatoryFrame,
        values = ["until", "for", "undetermined"],
        state="readonly"
    )
    repeatCombobox.grid(row=0, column=3, rowspan=2, sticky=tk.NE)

    untilCalendar = tkc.DateEntry(
        mandatoryFrame,
        selectmode="day",
        date_pattern="y/mm/dd"
    )
    untilCalendar._top_cal.lift()

    countValue = tk.IntVar(value=0)
    countLabel = ttk.Label(mandatoryFrame, text=" times")
    countSpinbox = ttk.Spinbox(mandatoryFrame, from_=0, increment=1, width=3, justify=tk.RIGHT, textvariable=countValue)

    repetitionType = tk.StringVar(value="undetermined")
    def displayRepetition(event):
        selected_value = event.widget.get()
        match selected_value:
            case "until":
                countSpinbox.grid_forget()
                countLabel.grid_forget()
                untilCalendar.grid(row=0, column=4, columnspan=2, rowspan=2, sticky=tk.N)
                repetitionType.set("until")
            case "for":
                untilCalendar.grid_forget()
                countSpinbox.grid(row=0, column=4, rowspan=2, sticky=tk.N)
                countLabel.grid(row=0, column=5, rowspan=2, sticky=tk.N)
                repetitionType.set("count")
            case "undetermined":
                countLabel.grid_forget()
                countSpinbox.grid_forget()
                untilCalendar.grid_forget()
                repetitionType.set("forever")
            case _:
                raise Exception(f"This error shouldn't be displayed")
    repeatCombobox.bind("<<ComboboxSelected>>", displayRepetition)
    mandatoryFrame.pack(fill="x")

    frames = [{"frame": None, "values": None}] * 7
    rulesFrameContainer = ttk.Frame(frame)
    def displayFreqFrame(event):
        for elt in frames:
            if elt["frame"]:
                elt["frame"].pack_forget()
        
        selected_value = event.widget.get()
        print(f"{selected_value=}")
        match selected_value:
            case "yearly":
                if (not frames[0]["frame"]):
                    print("No frame yet")
                    frames[0]["frame"] = makeRuleFrame(rulesFrameContainer, selected_value, False)
                frames[0]["frame"].pack(fill="x")
            case _:
                print("No no")

        pass
    frequencyCombobox.bind("<<ComboboxSelected>>", displayFreqFrame)

    #     match selected_value:
    #         case "yearly":
    #             if (not frames[0]["frame"]):
    #                 frames[0]["frame"] = makeRuleFrame(rulesFrame, selected_value)
    #             frames[0]["frame"].pack(fill="x")
    #         case "monthly":
    #             if (not frames[1]["frame"]):
    #                 frames[1]["frame"] = makeRuleFrame(rulesFrame, selected_value)
    #             frames[1]["frame"].pack(fill="x")
    #         case _:
    #             raise Exception(f"Unimplemented")
    #     tmp = makeRuleFrame(frame, selected_value, False)
    #     tmp.pack(fill="x")

    rulesFrameContainer.pack(fill="x")

    valueHolder = {
        "freq": freqValue,
        "repetition": repetitionType,
        "until": None,
        "count": countValue,
        "interval": intervalValue,
        "bysecond": None,
        "byminute": None,
        "byhour": None,
        "byday": None,
        "bymonthday": None,
        "byyearday": None,
        "byweekno": None,
        "bymonth":None,
        "bysetpos": None,
        "time_included": time_included
    }

    return frame, valueHolder

# def makeByXxxFrame(root: tk.Frame, userChoice: str) -> tk.Listbox :
#     xxx = ""
#     match userChoice:
#         case "day number of the month":
#             xxx = "monthday"
#         case "day number of the year":
#             xxx = "yearday"
#         case "week number of the year":
#             xxx = "yearday"
#         case "month number of the year":
#             xxx = "month"
#         case "hour"|"minute"|"second":
#             raise Exception(f"{userChoice} hasn't been implement yet")
#         case _:
#             raise Exception(f"Invalid user choice")
#     xxxList = [
#         "sec",
#         "minute",
#         "hour",
#         "day",
#         "monthday",
#         "yearday",
#         "weekno",
#         "month",
#         "setpos"
#     ]
#     if (not xxx in xxxList):
#         raise Exception(f"by{xxx} is not a valid byXxx list")
# 
#     frame = ttk.Frame(root)
#     config = configuration["rrule"][f"{xxx}"]
#     choices = []
#     if (xxx in ["month", "day"]):
#         choices = config["choices"]
#     else:
#         choices = [i for i in range (config["min"], config["max"]+1, config["step"])]
# 
#     listbox = tk.Listbox(frame, listvariable=tk.Variable(value=choices), height=5, selectmode="multiple")
#     listbox.pack(side="left")
#     ttk.Label(frame, text=configuration["rrule"][f"{xxx}"]["label"]).pack(side="right")
# 
#     result = {
#         "frame": frame,
#         "xxx": xxx,
#         "listbox": listbox
#     }
# 
#     return result
# 
# def makeRuleFrame(root: tk.Frame, freq: str, removable: bool = True, remaining: int = 0):
#     frame = ttk.Frame(root)
#     frame.rowconfigure(1)
#     for i in range (5):
#         frame.columnconfigure(i, weight=1)
#     ttk.Label(frame, text="Rule: ").grid(row=0, column=0, sticky=tk.W)
# 
#     choices = None
#     match freq:
#         case "yearly":
#             choices = ["day number of the month", "day number of the year", "week number of the year", "month"]
#         case "monthly":
#             choices = ["day number of the month", "month"]
#         case "weekly"|"daily"|"hourly"|"minutely"|"secondly":
#             raise NotImplementedError()
#         case _:
#             raise Exception(f"{freq} is not a valid frequence")
#     combobox = ttk.Combobox(
#         frame,
#         values=choices,
#         exportselection=False
#     )
#     combobox.grid(row=0, column=1, sticky=tk.W)
# 
#     def makeXxxFrame(event):
#         selected_value = event.widget.get()
#         truc = makeByXxxFrame(frame, selected_value)
#         truc["frame"].grid(row=0, column=2)
# 
#     combobox.bind("<<ComboboxSelected>>", makeXxxFrame)
# 
#     def foo():
#         fooFrame = makeRuleFrame(root, freq)
#         fooFrame.pack(fill="x")
# 
#     if (removable):
#         ttk.Button(frame, text="-", command=frame.destroy).grid(row=0, column=3, sticky=tk.E)
#         ttk.Button(frame, text="+", command=foo).grid(row=0, column=4, sticky=tk.E)
#     else:
#         ttk.Button(frame, text="+", command=foo).grid(row=0, column=3, columnspan=2, sticky=tk.E)
#     return frame