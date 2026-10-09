from tkinter import ttk
import tkinter as tk
import tkcalendar as tkc
from datetime import datetime

from src.utils import configuration, findLangIdFromLangValue, logging
from src.gui.parameters import *

# NOTE: put the user input part in a hiddable frame iff the frame is optional for all the types of event it can appears

def makeAttachmentFrame(root):
    frame = tk.Frame(root)

    parameterFrame = tk.Frame(frame)
    entry = tk.Entry(parameterFrame)
    entry.pack()
    fmttypeFrame, fmttypeInput = makeFmtTypeFrame(parameterFrame)
    fmttypeFrame.pack()

    state = tk.BooleanVar(value=False)
    def toggleParameterFrame():
        if (state.get()):
            parameterFrame.pack()
            button.config(text="Attachment : ")
        else:
            parameterFrame.pack_forget()
            button.config(text="Attachment ? ")
    button = tk.Checkbutton(frame, text="Attachment ? ", variable=state, offvalue=False, onvalue=True, command=toggleParameterFrame)
    button.pack()

    valueHolder = {
        "state": state,
        "value": entry,
        "fmttype": fmttypeInput
    }
    return frame, valueHolder

def makeCategoriesFrame(root):
    frame = tk.Frame(root)

    label = tk.Label(frame, text="Categories: ")
    label.pack(side="left")

    listbox = tk.Listbox(
        frame,
        selectmode="multiple",
        height=min(configuration["categories"]["height"], len(configuration["categories"]["choices"]))
    )
    for i in range(len(configuration["categories"]["choices"])):
        listbox.insert(i, configuration["categories"]["choices"][i])
    listbox.pack()

    parameterFrame = tk.Frame(frame)
    userInput = tk.Entry(parameterFrame)
    userInput.pack()

    languageFrame, languageInput = makeLanguageFrame(parameterFrame)
    languageFrame.pack(side="bottom")

    def add():
        value = userInput.get()
        values = list(listbox["values"])
        if value and value not in values:
            values.append(value)
            listbox["values"] = values
            userInput.delete(0, tk.END)
            listbox.set(listbox["values"][-1])

    def addToConfiguration():
        value = userInput.get()
        if value and value not in configuration["categories"]["choices"]:
            add()
            configuration["categories"]["choices"].append(value)

    def remove():
        value = listbox.get()
        values = list(listbox["values"])
        if value in values:
            values.remove(value)
            listbox["values"] = values
            listbox.delete(0, tk.END)
            if (len(listbox["values"]) != 0):
                listbox.set(values[0])
            else:
                listbox.set("")

    def removeFromConfiguration():
        value = combobox.get()
        if value in configuration["categories"]["choices"]:
            remove()
            configuration["cutype"]["choices"].remove(value)

    buttonsFrame = tk.Frame(parameterFrame)
    tk.Button(buttonsFrame, text="Add", command=add).pack()
    tk.Button(buttonsFrame, text="Add to configuration", command=addToConfiguration).pack()
    tk.Button(buttonsFrame, text="Remove", command=remove).pack()
    tk.Button(buttonsFrame, text="Remove from configuration", command=removeFromConfiguration).pack()
    buttonsFrame.pack(side="right")

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
        "listbox": listbox,
    }

    return frame, valueHolder

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

def makeStatusFrame(frame, componentType: str):
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

def makeSummaryFrame(frame, title):
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

def makeDtFrame(frame, typename: str):
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

def makeAttendeeFrame(frame, eventType: str):
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