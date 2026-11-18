from tkinter import ttk
from tktooltip import ToolTip
import tkinter as tk
import tkcalendar as tkc
from datetime import datetime

from src.utils import findLangIdFromLangValue
from src.gui.parameters import *
from src.gui.rrule import *

"""
- grid documentation: https://tkdocs.com/tutorial/grid.html

Some guidelines:
- manage the maximum of the properties frames features in the dedicated function, so the caller just has to grid it
"""

# create a frame for attachment property
def makeAttachmentFrame(root: tk.Frame, valueHolder: dict) -> tk.Frame :
    """
    create a frame for attachment property

    Params:
    ------
    - root: tk.Frame
        frame in which the newly created frame will be contained
    - valueHolder: dict
        dictionnary that will hold the entry widget

    Returns:
    -------
    - tk.Frame: the newly created attachment frame
    """
    frame = tk.Frame(root)
    frame.grid(sticky=[tk.W])
    frame.grid_remove()
    # label place
    frame.columnconfigure(0, weight=0)
    # value place
    frame.columnconfigure(1, weight=1)
    # tooltip place
    frame.columnconfigure(2, weight=0)
    frame.rowconfigure(0, weight=0)

    entry = tk.Entry(frame)
    entry.grid(row=0, column=1)
    entry.grid_remove()

    tooltipLabel = ttk.Label(frame, text=" ? ")
    tooltipLabel.grid(row=0, column=2)

    ToolTip(tooltipLabel, msg="Please enter a link to access the document", follow=True)

    state = tk.BooleanVar(value=False)
    def toggleParameterFrame():
        if (state.get()):
            button.config(text="Attachment : ")
            entry.grid()
        else:
            entry.grid_remove()
            button.config(text="Attachment ?")

    button = tk.Checkbutton(frame, text="Attachment ?", variable=state, offvalue=False, onvalue=True, command=toggleParameterFrame)
    button.grid(row=0, column=0)

    valueHolder["state"] = state
    valueHolder["value"] = entry

    return frame

def makeCategoriesFrame(root: tk.Frame, valueHolder: dict, configuration: dict) -> tk.Frame :
    # main frame
    frame = tk.Frame(root)
    frame.grid(sticky=[tk.W])
    frame.grid_remove()
    for i in range(3):
        frame.rowconfigure(i, weight=0)
    for i in range(4):
        frame.columnconfigure(i, weight=0)

    hiddableFrame = ttk.Frame(frame)
    for i in range(3):
        hiddableFrame.rowconfigure(i, weight=0)
    for i in range(3):
        hiddableFrame.columnconfigure(i, weight=0)
    hiddableFrame.grid(row=0, rowspan=3, column=1, columnspan=2)
    hiddableFrame.grid_remove()

    # display all the categories
    listbox = tk.Listbox(
        hiddableFrame,
        selectmode="multiple",
        height=min(configuration["height"], len(configuration["choices"]))
    )
    for i in range(len(configuration["choices"])):
        listbox.insert(i, configuration["choices"][i])
    listbox.grid(row=0, rowspan=3, column=0, sticky=[tk.N])
    def getChoices():
        return [listbox.get(index) for index in listbox.curselection()]
    valueHolder["value"] = getChoices

    entry = tk.StringVar()
    entryWidget = ttk.Entry(hiddableFrame, textvariable=entry)
    entryWidget.grid(row=0, column=1, columnspan=2, sticky=[tk.W, tk.E])
    # let the user add a new category for this particular component
    def add():
        value = entry.get()
        if (value and value not in listbox.get(0, tk.END)):
            listbox.insert(listbox.size(), value)
        listbox.config(height=min(configuration["height"], listbox.size()))
        entry.set(value="")
    addButton = tk.Button(hiddableFrame, text="Add", command=add)
    addButton.grid(row=1, column=1, sticky=[tk.W, tk.E])

    # let the user add a new category in the configuration
    def addToConfig():
        value = entry.get()
        if (value and value not in configuration["choices"]):
            configuration["choices"].append(value)
        add()
        entry.set(value="")
    addConfigButton = tk.Button(hiddableFrame, text="Add to configuration", command=addToConfig)
    addConfigButton.grid(row=1, column=2, sticky=[tk.W, tk.E])

    # let the user remove a category from the configuration
    def removeFromConfig():
        selection = listbox.curselection()
        for index in reversed(selection):
            configuration["choices"].pop(index)
        remove()
    removeConfigButton = tk.Button(hiddableFrame, text="Remove from configuration", command=removeFromConfig)
    removeConfigButton.grid(row=2, column=2, sticky=[tk.W, tk.E])

    # let the user remove a category for this particular component
    def remove():
        selection = listbox.curselection()
        for index in reversed(selection):
            listbox.delete(index)
    removeButton = tk.Button(hiddableFrame, text="Remove", command=remove)
    removeButton.grid(row=2, column=1, sticky=[tk.W, tk.E])

    # check button logic
    state = tk.BooleanVar(value=False)
    valueHolder["state"] = state
    def displayChoicesFrame():
        if (state.get()):
            hiddableFrame.grid()
            checkbutton.config(text="Categories: ")
            pass
        else:
            hiddableFrame.grid_remove()
            checkbutton.config(text="Categories ?")
            pass
    checkbutton = ttk.Checkbutton(frame, text="Categories ? ", variable=state, offvalue=False, onvalue=True, command=displayChoicesFrame)
    checkbutton.grid(row=0, column=0, sticky=[tk.N])

    return frame

    # frame.rowconfigure(0, weight=0)
    # frame.columnconfigure(0, weight=1)

    # label = ttk.Label(frame, text="Categories: ")
    # label.grid(row=0, column=0)

    # listbox = tk.Listbox(
    #     frame,
    #     selectmode="multiple",
    #     height=min(configuration["height"], len(configuration["choices"]))
    # )
    # for i in range(len(configuration["categories"]["choices"])):
    #     listbox.insert(i, configuration["categories"]["choices"][i])
    # listbox.pack()

    # parameterFrame = tk.Frame(frame)
    # userInput = tk.Entry(parameterFrame)
    # userInput.pack()

    # languageFrame, languageInput = makeLanguageFrame(parameterFrame)
    # languageFrame.pack(side="bottom")


    # def addToConfiguration():
    #     value = userInput.get()
    #     if value and value not in configuration["categories"]["choices"]:
    #         add()
    #         configuration["categories"]["choices"].append(value)

    # def remove():
    #     value = listbox.get()
    #     values = list(listbox["values"])
    #     if value in values:
    #         values.remove(value)
    #         listbox["values"] = values
    #         listbox.delete(0, tk.END)
    #         if (len(listbox["values"]) != 0):
    #             listbox.set(values[0])
    #         else:
    #             listbox.set("")

    # def removeFromConfiguration():
    #     value = combobox.get()
    #     if value in configuration["categories"]["choices"]:
    #         remove()
    #         configuration["cutype"]["choices"].remove(value)

    # buttonsFrame = tk.Frame(parameterFrame)
    # tk.Button(buttonsFrame, text="Add", command=add).pack()
    # tk.Button(buttonsFrame, text="Add to configuration", command=addToConfiguration).pack()
    # tk.Button(buttonsFrame, text="Remove", command=remove).pack()
    # tk.Button(buttonsFrame, text="Remove from configuration", command=removeFromConfiguration).pack()
    # buttonsFrame.pack(side="right")

    # state = tk.BooleanVar(value=False)
    # def toggleParameterFrame(event):
    #     actual = not state.get()
    #     if (state.get()):
    #         parameterFrame.pack()
    #     else:
    #         parameterFrame.pack_forget()
    #     state.set(actual)
    # label.bind('<Double-1>', toggleParameterFrame)

    # valueHolder = {
    #     "listbox": listbox,
    # }


def makeClassificationFrame(root):
    frame = tk.Frame(root)

    tk.Label(frame, text="Classification: ").pack(side="left")
    value = tk.StringVar(value="")
    combobox = ttk.Combobox(
        frame,
        values=configuration["classification"]["choices"],
        state="readonly",
        textvariable=value
    )
    combobox.pack()

    valueHolder = {
        "value": combobox
    }

    return frame, valueHolder

def makeCommentFrame(root):
    frame = tk.Frame(root)

    label = tk.Label(frame, text="Comment")
    label.pack()
    commentText = tk.Text(
        frame,
        height=configuration["comment"]["height"],
        width=configuration["comment"]["width"]
    )
    commentText.pack(expand=True, fill="both")

    parameterFrame = tk.Frame(frame)
    altrepFrame, altrepInput = makeAlternativeRepresentationFrame(parameterFrame)
    altrepFrame.pack()
    languageFrame, languageInput = makeLanguageFrame(parameterFrame)
    languageFrame.pack()

    state = tk.BooleanVar(value=False)
    def toggleParameterFrame(event):
        actual = not state.get()
        if (actual):
            parameterFrame.pack()
        else:
            parameterFrame.pack_forget()
        state.set(actual)
    label.bind('<Double-1>', toggleParameterFrame) 

    valueHolder = {
        "value": commentText,
        "state": state,
        "altrep": altrepInput,
        "language": languageInput
    }

    return frame, valueHolder

def makeDescriptionFrame(root):
    frame = tk.Frame(root)

    label = tk.Label(frame, text="Description")
    label.pack(anchor="w")
    descriptionText = tk.Text(frame)
    descriptionText.config(
        height=configuration["description"]["height"],
        width=configuration["description"]["width"]
    )
    descriptionText.pack()

    parameterFrame = tk.Frame(frame)
    altrepFrame, altrepInput = makeAlternativeRepresentationFrame(parameterFrame)
    altrepFrame.pack()
    languageFrame, languageInput = makeLanguageFrame(parameterFrame)
    languageFrame.pack()

    state = tk.BooleanVar(value=False)
    def toggleParameterFrame(event):
        actual = not state.get()
        if (state.get()):
            parameterFrame.pack()
        else:
            parameterFrame.pack_forget()
        state.set(actual)
    label.bind('<Double-1>', toggleParameterFrame)

    valueHolder = {
        "state": state,
        "value": descriptionText,
        "altrep": altrepInput,
        "language": languageInput
    }

    return frame, valueHolder

def makeGeoFrame(root):
    frame = tk.Frame(root)

    tk.Label(frame, text="Geographical position: ").pack(side="left")
    latVar = tk.StringVar(value=None)
    latSpinbox = ttk.Spinbox(frame, from_=-90.000000, to=90.000000, wrap=True, increment=0.000001, textvariable=latVar)
    latSpinbox.pack(side="right")
    tk.Label(frame, text=" ; ").pack(side="right")
    longVar = tk.StringVar(value=None)
    longSpinbox = ttk.Spinbox(frame, from_=-180.000000, to=180.000000, wrap=True, increment=0.000001, textvariable=longVar)
    longSpinbox.pack(side="right")

    valueHolder = {
        "lat": latVar,
        "long": longVar
    }

    return frame, valueHolder

def makeLocationFrame(root):
    frame = tk.Frame(root)

    state = tk.BooleanVar(value=False)
    parameterFrame = tk.Frame(frame)
    altrepFrame, altrepInput = makeAlternativeRepresentationFrame(parameterFrame)
    altrepFrame.pack()
    languageFrame, languageInput = makeLanguageFrame(parameterFrame)
    languageFrame.pack()


    label = tk.Label(frame, text="Location: ")
    label.pack(side="left")
    def toggleParameterFrame(event):
        actual = state.get()
        actual = not actual
        if (actual):
            parameterFrame.pack(side="bottom")
        else:
            parameterFrame.pack_forget()
        state.set(actual)

    label.bind('<Double-1>', toggleParameterFrame)

    locationText = tk.Text(frame)
    locationText.config(
        height=configuration["location"]["height"],
        width=configuration["location"]["width"]
    )
    locationText.pack(side="left")

    valueHolder = {
        "value": locationText,
        "state": state,
        "altrep": altrepInput,
        "language": languageInput
    }

    return frame, valueHolder

def makePercentFrame(root):
    frame = tk.Frame(root)

    parameterFrame = tk.Frame(frame)
    percentVar = tk.StringVar(value="")
    tk.Label(parameterFrame, text=" %").pack(side="right")
    latSpinbox = ttk.Spinbox(parameterFrame, from_=0, to=100, increment=1, textvariable=percentVar)
    latSpinbox.pack(side="right")

    state = tk.BooleanVar(value=False)
    def toggleParameterFrame():
        if (state.get()):
            button.config(text="Task completed at ")
            parameterFrame.pack(side="right")
        else:
            button.config(text="Completed ? ")
            parameterFrame.pack_forget()
    button = tk.Checkbutton(frame, text="Completed ? ", variable=state, offvalue=False, onvalue=True, command=toggleParameterFrame)
    button.pack(side="left")

    valueHolder = {
        "state": state,
        "value": percentVar
    }

    return frame, valueHolder

def makePriorityFrame(root):
    frame = tk.Frame(root)

    tk.Label(frame, text="Priority level: ").pack(side="left")
    priorityVar = tk.StringVar(value="")
    prioritySpinbox = ttk.Spinbox(frame, from_=0, to=9, increment=1, textvariable=priorityVar, wrap=True)
    prioritySpinbox.pack(side="right")

    valueHolder = {
        "value": priorityVar
    }

    return frame, valueHolder

def makeResourceFrame(root):
    frame = tk.Frame(root)

    parameterFrame = tk.Frame(frame)
    resourceText = tk.Text(parameterFrame)
    resourceText.config(
        height=configuration["resources"]["height"],
        width=configuration["resources"]["width"]
    )
    resourceText.pack()

    altrepFrame, altrepInput = makeAlternativeRepresentationFrame(parameterFrame)
    altrepFrame.pack()

    languageFrame, languageInput = makeLanguageFrame(parameterFrame)
    languageFrame.pack()

    state = tk.BooleanVar(value=False)
    def toggleParameterFrame():
        if (state.get()):
            button.config(text="Resource : ")
            parameterFrame.pack()
        else:
            button.config(text="Resource ? ")
            parameterFrame.pack_forget()
    button = tk.Checkbutton(frame, text="Resource ? ", variable=state, offvalue=False, onvalue=True, command=toggleParameterFrame)
    button.pack()

    valueHolder = {
        "state": state,
        "value": resourceText,
        "altrep": altrepInput,
        "language": languageInput
    }

    return frame, valueHolder

def makeStatusFrame(root, componentType: str):
    frame = tk.Frame(root)

    value = tk.StringVar(value="")
    statusCombobox = ttk.Combobox(
        frame,
        values=configuration["status"][f"{componentType}"],
        state="readonly",
        textvariable=value
    )
    statusCombobox.pack()

    return frame, value

def makeSummaryFrame(root, title):
    frame = tk.Frame(root)

    label = tk.Label(frame, text="Title: ")
    label.pack(side="left")

    summaryEntry = tk.Entry(frame, textvariable=title)
    summaryEntry.pack(side="left")
    
    parameterFrame = tk.Frame(frame)
    altrepFrame, altrepInput = makeAlternativeRepresentationFrame(parameterFrame)
    altrepFrame.pack()
    languageFrame, languageInput = makeLanguageFrame(parameterFrame)
    languageFrame.pack()

    state = tk.BooleanVar(value=False)
    def toggleParameterFrame(event):
        actual = not state.get()
        if (actual):
            logging.debug(f"User toggled hiddable frame from a {title.get()} event frame.")
            parameterFrame.pack(side="bottom")
        else:
            parameterFrame.pack_forget()
            logging.debug(f"User untoggled hiddable frame from a {title.get()} event frame.")
        state.set(actual)
    label.bind('<Double-1>', toggleParameterFrame)

    valueHolder = {
        "value": title,
        "state": state,
        "altrep": altrepInput,
        "language": languageInput
    }

    return frame, valueHolder

def makeDtFrame(root, typename: str):
    # typename is the name of the type of the datime
    if (typename not in ["completed", "end", "due", "start"]):
        return None, None

    dtFrame = tk.Frame(root)

    if (typename == "start"):
        tk.Label(dtFrame, text="From ").pack(side="left")
    elif (typename == "end"):
        tk.Label(dtFrame, text="to ").pack(side="left")
    elif (typename == "due"):
        tk.Label(dtFrame, text="Due for ").pack(side="left")
    elif (typename == "completed"):
            tk.Label(dtFrame, text="Completed on ").pack(side="left")
    today = datetime.now()
    dateEntry = tkc.DateEntry(
        dtFrame,
        selectmode="day",
        date_pattern="y/mm/dd"
    )
    dateEntry.pack(side="left")
    # line below is mandatroy: let the calendar be clickable even if there is a widget below it on the z-axis
    dateEntry._top_cal.lift()

    timeFrame = tk.Frame(dtFrame)
    secondVar = tk.StringVar(value="0")
    secondSpinbox = tk.Spinbox(
        timeFrame,
        from_=0,
        to=59,
        increment=1,
        width=2,
        textvariable=secondVar,
        justify=tk.RIGHT
    )
    minuteVar = tk.StringVar(value="")
    minuteSpinbox = tk.Spinbox(
        timeFrame,
        from_=0,
        to=59,
        increment=1,
        width=2,
        textvariable=minuteVar ,
        justify=tk.RIGHT

    )
    hourVar = tk.StringVar(value="9")
    hourSpinbox = tk.Spinbox(
        timeFrame,
        from_=0,
        to=23,
        increment=1,
        width=2,
        textvariable=hourVar,
        justify=tk.RIGHT

    )
    tk.Label(timeFrame, text="s").pack(side="right")
    secondSpinbox.pack(side="right")
    tk.Label(timeFrame, text="m ").pack(side="right")
    minuteSpinbox.pack(side="right")
    tk.Label(timeFrame, text="h ").pack(side="right")
    hourSpinbox.pack(side="right")

    timestate = tk.BooleanVar(value=
        configuration[f"general"]["time-status"] or configuration[f"dt{typename}"]["datetime-default"]
    )
    def toggleHiddableTimeFrame():
        if (timestate.get()):
            timebutton.config(text=" at ")
            timeFrame.pack(side="right")
        else:
            timebutton.config(text="Time ? ")
            timeFrame.pack_forget()
    timebutton = tk.Checkbutton(dtFrame, text="Time ? ", variable=timestate, offvalue=False, onvalue=True, command=toggleHiddableTimeFrame)
    timebutton.pack(side="left")
    if (timestate.get()):
        timebutton.config(text=" at ")
        timeFrame.pack(side="right")

    valueHolder = {
        "date": dateEntry,
        "time-status": timestate,
        "hour": hourVar,
        "minute": minuteVar,
        "second": secondVar
    }

    return dtFrame, valueHolder

def makeDurationFrame(root):
    frame = tk.Frame(root)

    week = tk.StringVar(value="0")
    weekEntry = tk.Spinbox(frame, textvariable=week, width=3, from_=0, wrap=True, justify=tk.RIGHT)
    weekEntry.pack(side="left")
    tk.Label(frame, text=configuration["duration"]["week-text"]).pack(side="left")
    day = tk.StringVar(value="")
    dayEntry = tk.Spinbox(frame, textvariable=day, width=2, from_=0, to=31, wrap=True, justify=tk.RIGHT)
    dayEntry.pack(side="left")
    tk.Label(frame, text=configuration["duration"]["day-text"]).pack(side="left")
    hour = tk.StringVar(value="")
    hourEntry = tk.Spinbox(frame, textvariable=hour, width=2, from_=0, to=23, wrap=True, justify=tk.RIGHT)
    hourEntry.pack(side="left")
    tk.Label(frame, text=configuration["duration"]["hour-text"]).pack(side="left")
    minute = tk.StringVar(value="")
    minuteEntry = tk.Spinbox(frame, textvariable=minute, width=2, from_=0, to=59, wrap=True, justify=tk.RIGHT)
    minuteEntry.pack(side="left")
    tk.Label(frame, text=configuration["duration"]["minute-text"]).pack(side="left")
    second = tk.StringVar(value="")
    secondEntry = tk.Spinbox(frame, textvariable=second, width=2, from_=0, to=59, wrap=True, justify=tk.RIGHT)
    secondEntry.pack(side="left")
    tk.Label(frame, text=configuration["duration"]["second-text"]).pack(side="left")

    valueHolder = {
        "week": week,
        "day": day,
        "hour": hour,
        "minute": minute,
        "second": second
    }

    return frame, valueHolder

def makeTranspFrame(root):
    frame = tk.Frame(root)

    value = tk.StringVar(value=configuration["transparency"]["choices"][0])
    tk.Label(frame, text="Transparency of the event: ").pack(side="left")
    transpCombobox = ttk.Combobox(
        frame,
        values=configuration["transparency"]["choices"],
        state="readonly",
        textvariable=value
    )
    transpCombobox.pack()

    return frame, value

def makeOrganizerFrame(root):
    frame = ttk.Frame(root)

    label = ttk.Label(frame, text="Organizer: ")
    label.pack(side="left")

    value = tk.StringVar(value="")
    combobox = ttk.Combobox(
        frame,
        values=[elt["common-name"] for elt in configuration["attendees"]["choices"]],
        exportselection=False,
        height=min(configuration["attendees"]["height"], len(configuration["attendees"]["choices"])),
        textvariable=value
    )
    combobox.pack(side="right")

    return frame, value

def makeAttendeeFrame(root, eventType: str):
    frame = tk.Frame(root)

    label = tk.Label(frame, text=f"Attendees: ")
    label.pack(side="left")
    listbox = tk.Listbox(
        frame,
        selectmode="multiple",
        exportselection=False,
        height=min(configuration["attendees"]["height"], len(configuration["attendees"]["choices"]))
    )

    for i in range(len(configuration["attendees"]["choices"])):
        listbox.insert(i, configuration["attendees"]["choices"][i]["common-name"])

    listbox.pack()

    # parameterFrame = tk.Frame(root)
    # cutypeFrame, cutypeDict = makeCutypeFrame(parameterFrame)
    # cutypeFrame.pack()
    # memberFrame, memberDict = makeMemberFrame(parameterFrame)
    # memberFrame.pack()
    # roleFrame, roleDict = makeRoleFrame(parameterFrame)
    # roleFrame.pack()
    # partstatFrame, parstatDict = makePartstatFrame(parameterFrame, eventType)
    # partstatFrame.pack()
    # rsvpFrame, rsvpDict = makeRsvpFrame(parameterFrame)
    # rsvpFrame.pack()
    # deltoFrame, deltoDict = makeDelegatedToFrame(parameterFrame)
    # deltoFrame.pack()
    # delfromFrame, delfromDict = makeDelegatedFromFrame(parameterFrame)
    # delfromFrame.pack()
    # sentbyFrame, sentbyDict = makeSentByFrame(parameterFrame)
    # sentbyFrame.pack()
    # cnFrame, cnDict = makeCommonNameFrame(parameterFrame)
    # cnFrame.pack()
    # dirFrame, dirDict = makeDirFrame(parameterFrame)
    # dirFrame.pack() 
    # languageFrame, languageDict = makeLanguageFrame(parameterFrame)
    # languageFrame.pack()

    # state = tk.BooleanVar(value=False)
    # def toggleParameterFrame(event):
    #     actual = not state.get()
    #     if (actual):
    #         parameterFrame.pack(side="bottom")
    #     else:
    #         parameterFrame.pack_forget()
    #     state.set(actual)
    # label.bind('<Double-1>', toggleParameterFrame)

    return frame, listbox

def makeURLFrame(master):
    frame = tk.Frame(master)

    tk.Label(frame, text="URL: ").pack(side="left")
    value = tk.StringVar(value="")
    entry = tk.Entry(frame, textvariable=value)
    entry.pack(side="right")

    return frame, value

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