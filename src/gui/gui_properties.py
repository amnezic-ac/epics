from tkinter import ttk
import tkinter as tk
from src.gui.gui_parameters import *
import tkcalendar as tkc
from datetime import datetime
from utils import configuration, logging

# NOTE: put the user input part in a hiddable frame iff the frame is optional for all the types of event it can appears

def makeAttachmentFrame(masterFrame):
    attachmentFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(attachmentFrame)
    attachmentValue = tk.Entry(hiddableFrame)
    attachmentValue.pack()
    fmttypeFrame, fmttypeInput = makeFmtTypeFrame(hiddableFrame)
    fmttypeFrame.pack()

    buttonState = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (buttonState.get()):
            hiddableFrame.pack()
            checkbutton.config(text="Attachment : ")
        else:
            hiddableFrame.pack_forget()
            checkbutton.config(text="Attachment ? ")
    checkbutton = tk.Checkbutton(attachmentFrame, text="Attachment ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    checkbutton.pack()

    attachmentDict = {
        "state": buttonState,
        "value": attachmentValue,
        "fmttype": fmttypeInput
    }
    return attachmentFrame, attachmentDict

def makeCategoriesFrame(masterFrame):
    categoriesFrame = tk.Frame(masterFrame)

    label = tk.Label(categoriesFrame, text="Categories: ")
    label.pack(side="left")

    listbox = tk.Listbox(
        categoriesFrame,
        selectmode="multiple",
        height=min(configuration["categories"]["height"], len(configuration["categories"]["choices"]))
    )
    for i in range(len(configuration["categories"]["choices"])):
        listbox.insert(i, configuration["categories"]["choices"][i])
    listbox.pack()

    hiddableFrame = tk.Frame(categoriesFrame)
    userInput = tk.Entry(hiddableFrame)
    userInput.pack()

    languageFrame, languageInput = makeLanguageFrame(hiddableFrame)
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

    buttonsFrame = tk.Frame(hiddableFrame)
    tk.Button(buttonsFrame, text="Add", command=add).pack()
    tk.Button(buttonsFrame, text="Add to configuration", command=addToConfiguration).pack()
    tk.Button(buttonsFrame, text="Remove", command=remove).pack()
    tk.Button(buttonsFrame, text="Remove from configuration", command=removeFromConfiguration).pack()
    buttonsFrame.pack(side="right")

    buttonState = tk.BooleanVar(value=False)
    def toggleHiddableFrame(event):
        actual = not buttonState.get()
        if (buttonState.get()):
            hiddableFrame.pack()
        else:
            hiddableFrame.pack_forget()
        buttonState.set(actual)
    label.bind('<Double-1>', toggleHiddableFrame)

    categoriesDict = {
        "listbox": listbox,
    }

    return categoriesFrame, categoriesDict

def makeClassificationFrame(masterFrame):
    classificationFrame = tk.Frame(masterFrame)

    tk.Label(classificationFrame, text="Classification").pack(side="left")
    value = tk.StringVar(value="")
    combobox = ttk.Combobox(
        classificationFrame,
        values=configuration["classification"]["choices"],
        state="readonly",
        textvariable=value
    )
    combobox.pack()

    classificationDict = {
        "value": combobox
    }

    return classificationFrame, classificationDict

def makeCommentFrame(masterFrame, configuration):
    commentFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(commentFrame)
    commentText = tk.Text(
        hiddableFrame,
        height=configuration["comment"]["height"],
        width=configuration["comment"]["width"]
    )
    commentText.pack()

    altrepFrame, altrepInput = makeAlternativeRepresentationFrame(hiddableFrame)
    altrepFrame.pack()

    languageFrame, languageInput = makeLanguageFrame(hiddableFrame)
    languageFrame.pack()

    buttonState = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (buttonState.get()):
            checkbutton.config(text="Comment : ")
            hiddableFrame.pack()
        else:
            checkbutton.config(text="Comment ? ")
            hiddableFrame.pack_forget()
    checkbutton = tk.Checkbutton(commentFrame, text="Comment ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    checkbutton.pack()

    commentDict = {
        "state": buttonState,
        "value": commentText,
        "altrep": altrepInput,
        "language": languageInput
    }

    return commentFrame, commentDict

def makeDescriptionFrame(masterFrame):
    descriptionFrame = tk.Frame(masterFrame)

    label = tk.Label(descriptionFrame, text="Description")
    label.pack(anchor="w")
    descriptionText = tk.Text(descriptionFrame)
    descriptionText.config(
        height=configuration["description"]["height"],
        width=configuration["description"]["width"]
    )
    descriptionText.pack()

    hiddableFrame = tk.Frame(descriptionFrame)
    altrepFrame, altrepInput = makeAlternativeRepresentationFrame(hiddableFrame)
    altrepFrame.pack()
    languageFrame, languageInput = makeLanguageFrame(hiddableFrame)
    languageFrame.pack()

    buttonState = tk.BooleanVar(value=False)
    def toggleHiddableFrame(event):
        actual = not buttonState.get()
        if (buttonState.get()):
            hiddableFrame.pack()
        else:
            hiddableFrame.pack_forget()
        buttonState.set(actual)
    label.bind('<Double-1>', toggleHiddableFrame)

    descriptionDict = {
        "state": buttonState,
        "value": descriptionText,
        "altrep": altrepInput,
        "language": languageInput
    }

    return descriptionFrame, descriptionDict

def makeGeoFrame(masterFrame):
    geoFrame = tk.Frame(masterFrame)

    tk.Label(geoFrame, text="Geographical position: ").pack(side="left")
    latVar = tk.StringVar(value=None)
    latSpinbox = ttk.Spinbox(geoFrame, from_=-90.000000, to=90.000000, wrap=True, increment=0.000001, textvariable=latVar)
    latSpinbox.pack(side="right")
    tk.Label(geoFrame, text=" ; ").pack(side="right")
    longVar = tk.StringVar(value=None)
    longSpinbox = ttk.Spinbox(geoFrame, from_=-180.000000, to=180.000000, wrap=True, increment=0.000001, textvariable=longVar)
    longSpinbox.pack(side="right")

    geoDict = {
        "lat": latVar,
        "long": longVar
    }

    return geoFrame, geoDict

def makeLocationFrame(masterFrame):
    locationFrame = tk.Frame(masterFrame)

    state = tk.BooleanVar(value=False)
    hiddableFrame = tk.Frame(locationFrame)
    altrepFrame, altrepInput = makeAlternativeRepresentationFrame(hiddableFrame)
    altrepFrame.pack()
    languageFrame, languageInput = makeLanguageFrame(hiddableFrame)
    languageFrame.pack()


    label = tk.Label(locationFrame, text="Location: ")
    label.pack(side="left")
    def toggleHiddableFrame(event):
        actual = state.get()
        actual = not actual
        if (actual):
            hiddableFrame.pack(side="bottom")
        else:
            hiddableFrame.pack_forget()
        state.set(actual)

    label.bind('<Double-1>', toggleHiddableFrame)

    locationText = tk.Text(locationFrame)
    locationText.config(
        height=configuration["location"]["height"],
        width=configuration["location"]["width"]
    )
    locationText.pack(side="left")

    locationDict = {
        "value": locationText,
        "state": state,
        "altrep": altrepInput,
        "language": languageInput
    }

    return locationFrame, locationDict

def makePercentFrame(masterFrame):
    percentFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(percentFrame)
    percentVar = tk.StringVar(value="")
    tk.Label(hiddableFrame, text=" %").pack(side="right")
    latSpinbox = ttk.Spinbox(hiddableFrame, from_=0, to=100, increment=1, textvariable=percentVar)
    latSpinbox.pack(side="right")

    buttonState = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (buttonState.get()):
            checkbutton.config(text="Task completed at ")
            hiddableFrame.pack(side="right")
        else:
            checkbutton.config(text="Completed ? ")
            hiddableFrame.pack_forget()
    checkbutton = tk.Checkbutton(percentFrame, text="Completed ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    checkbutton.pack(side="left")

    percentDict = {
        "state": buttonState,
        "value": percentVar
    }

    return percentFrame, percentDict

def makePriorityFrame(masterFrame):
    priorityFrame = tk.Frame(masterFrame)

    tk.Label(priorityFrame, text="Priority level: ").pack(side="left")
    priorityVar = tk.StringVar(value="")
    prioritySpinbox = ttk.Spinbox(priorityFrame, from_=0, to=9, increment=1, textvariable=priorityVar, wrap=True)
    prioritySpinbox.pack(side="right")

    priorityDict = {
        "value": priorityVar
    }

    return priorityFrame, priorityDict

def makeResourceFrame(masterFrame, configuration):
    resourceFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(resourceFrame)
    resourceText = tk.Text(hiddableFrame)
    resourceText.config(
        height=configuration["resources"]["height"],
        width=configuration["resources"]["width"]
    )
    resourceText.pack()

    altrepFrame, altrepInput = makeAlternativeRepresentationFrame(hiddableFrame)
    altrepFrame.pack()

    languageFrame, languageInput = makeLanguageFrame(hiddableFrame)
    languageFrame.pack()

    buttonState = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (buttonState.get()):
            checkbutton.config(text="Resource : ")
            hiddableFrame.pack()
        else:
            checkbutton.config(text="Resource ? ")
            hiddableFrame.pack_forget()
    checkbutton = tk.Checkbutton(resourceFrame, text="Resource ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    checkbutton.pack()

    resourceDict = {
        "state": buttonState,
        "value": resourceText,
        "altrep": altrepInput,
        "language": languageInput
    }

    return resourceFrame, resourceDict

def makeStatusFrame(masterFrame, componentType: str):
    statusFrame = tk.Frame(masterFrame)

    value = tk.StringVar(value=configuration["status"][f"{componentType}"][0])
    statusCombobox = ttk.Combobox(
        statusFrame,
        values=configuration["status"][f"{componentType}"],
        state="readonly",
        textvariable=value
    )
    statusCombobox.pack()

    return statusFrame, value

def makeSummaryFrame(masterFrame, title):
    summaryFrame = tk.Frame(masterFrame)

    tk.Label(summaryFrame, text="Title: ").pack(side="left")

    summaryEntry = tk.Entry(summaryFrame, textvariable=title)
    summaryEntry.pack(side="left")
    
    hiddableFrame = tk.Frame(summaryFrame)
    altrepFrame, altrepInput = makeAlternativeRepresentationFrame(hiddableFrame)
    altrepFrame.pack()

    languageFrame, languageInput = makeLanguageFrame(hiddableFrame)
    languageFrame.pack()
    
    state = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (state.get()):
            logging.debug(f"User toggled hiddable frame from a {title.get()} event frame.")
            hiddableFrame.pack(side="bottom")
        else:
            hiddableFrame.pack_forget()
            logging.debug(f"User untoggled hiddable frame from a {title.get()} event frame.")
    button = tk.Checkbutton(summaryFrame, text="+", variable=state, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    button.pack(side="right")

    summaryDict = {
        "value": title,
        "state": state,
        "altrep": altrepInput,
        "language": languageInput
    }

    return summaryFrame, summaryDict

def makeDtFrame(masterFrame, typename: str):
    # typename is the name of the type of the datime
    if (typename not in ["completed", "end", "due", "start"]):
        return None, None

    dtFrame = tk.Frame(masterFrame)

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

    timeFrame = tk.Frame(dtFrame)
    secondVar = tk.StringVar(value="0")
    secondSpinbox = tk.Spinbox(
        timeFrame,
        from_=0,
        to=59,
        increment=1,
        width=4,
        textvariable=secondVar
    )
    minuteVar = tk.StringVar(value="0")
    minuteSpinbox = tk.Spinbox(
        timeFrame,
        from_=0,
        to=59,
        increment=1,
        width=4,
        textvariable=minuteVar 
    )
    hourVar = tk.StringVar(value="0")
    hourSpinbox = tk.Spinbox(
        timeFrame,
        from_=0,
        to=23,
        increment=1,
        width=4,
        textvariable=hourVar
    )
    tk.Label(timeFrame, text="s").pack(side="right")
    secondSpinbox.pack(side="right")
    tk.Label(timeFrame, text="m ").pack(side="right")
    minuteSpinbox.pack(side="right")
    tk.Label(timeFrame, text="h ").pack(side="right")
    hourSpinbox.pack(side="right")

    timebuttonState = tk.BooleanVar(value=
        configuration[f"general"]["time-status"] or configuration[f"dt{typename}"]["datetime-default"]
    )
    def toggleHiddableTimeFrame():
        if (timebuttonState.get()):
            timecheckbutton.config(text=" at ")
            timeFrame.pack(side="right")
        else:
            timecheckbutton.config(text="Time ? ")
            timeFrame.pack_forget()
    timecheckbutton = tk.Checkbutton(dtFrame, text="Time ? ", variable=timebuttonState, offvalue=False, onvalue=True, command=toggleHiddableTimeFrame)
    timecheckbutton.pack(side="left")
    if (timebuttonState.get()):
        timecheckbutton.config(text=" at ")
        timeFrame.pack(side="right")

    dtDict = {
        "date": dateEntry,
        "time-status": timebuttonState,
        "hour": hourVar,
        "minute": minuteVar,
        "second": secondVar
    }

    return dtFrame, dtDict

def makeDurationFrame(masterFrame, configuration):
    durationFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(durationFrame)

    week = tk.StringVar(value="0")
    weekEntry = tk.Spinbox(hiddableFrame, textvariable=week, width=3, from_=0, wrap=True)
    weekEntry.pack(side="left")
    tk.Label(hiddableFrame, text=configuration["duration"]["week-text"]).pack(side="left")
    day = tk.StringVar(value="")
    dayEntry = tk.Spinbox(hiddableFrame, textvariable=day, width=3, from_=0, to=31, wrap=True)
    dayEntry.pack(side="left")
    tk.Label(hiddableFrame, text=configuration["duration"]["day-text"]).pack(side="left")
    hour = tk.StringVar(value="")
    hourEntry = tk.Spinbox(hiddableFrame, textvariable=hour, width=3, from_=0, to=23, wrap=True)
    hourEntry.pack(side="left")
    tk.Label(hiddableFrame, text=configuration["duration"]["hour-text"]).pack(side="left")
    minute = tk.StringVar(value="")
    minuteEntry = tk.Spinbox(hiddableFrame, textvariable=minute, width=3, from_=0, to=59, wrap=True)
    minuteEntry.pack(side="left")
    tk.Label(hiddableFrame, text=configuration["duration"]["minute-text"]).pack(side="left")
    second = tk.StringVar(value="")
    secondEntry = tk.Spinbox(hiddableFrame, textvariable=second, width=3, from_=0, to=59, wrap=True)
    secondEntry.pack(side="left")
    tk.Label(hiddableFrame, text=configuration["duration"]["second-text"]).pack(side="left")

    state = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (state.get()):
            hiddableFrame.pack(side="right")
            button.config(text="Duration : ")
        else:
            button.config(text="Duration ? ")
            hiddableFrame.pack_forget()
    button = tk.Checkbutton(durationFrame, text="Duration ? ", variable=state, onvalue=True, offvalue=False, command=toggleHiddableFrame)
    button.pack(side="left")

    duration = {
        "value": state,
        "week": week,
        "day": day,
        "hour": hour,
        "minute": minute,
        "second": second
    }

    return durationFrame, duration

def makeTranspFrame(masterFrame):
    transpFrame = tk.Frame(masterFrame)

    value = tk.StringVar(value=configuration["transparency"]["choices"][0])
    tk.Label(transpFrame, text="Transparency of the event: ").pack(side="left")
    transpCombobox = ttk.Combobox(
        transpFrame,
        values=configuration["transparency"]["choices"],
        state="readonly",
        textvariable=value
    )
    transpCombobox.pack()

    transpDict = {
        "value": value
    }

    return transpFrame, transpDict

def makeAttendeeFrame(masterFrame, eventType: str, labelText: str):
    attendeeFrame = tk.Frame(masterFrame)

    userFrame = tk.Frame(attendeeFrame)

    hiddableFrame = tk.Frame(attendeeFrame)
    cutypeFrame, cutypeDict = makeCutypeFrame(hiddableFrame, configuration)
    cutypeFrame.pack()

    label = tk.Label(attendeeFrame, text=f"{labelText}")
    state = tk.BooleanVar(value=False)
    def toggleHiddableFrame(event):
        actual = not state.get()
        if (actual):
            hiddableFrame.pack(side="bottom")
        else:
            hiddableFrame.pack_forget()
        state.set(actual)

    label.bind('<Double-1>', toggleHiddableFrame)
    label.pack(side="left")

    value = tk.StringVar(value="ORGANIZER ENTRY (TODO)")
    userInput = tk.Entry(attendeeFrame, textvariable=value)
    userInput.pack()

    # memberFrame, memberDict = makeMemberFrame(hiddableFrame, configuration)
    # memberFrame.pack()
    # roleFrame, roleDict = makeRoleFrame(hiddableFrame, configuration)
    # roleFrame.pack()
    # partstatFrame, parstatDict = makePartstatFrame(hiddableFrame, configuration, eventType)
    # partstatFrame.pack()
    # rsvpFrame, rsvpDict = makeRsvpFrame(hiddableFrame, configuration)
    # rsvpFrame.pack()
    # deltoFrame, deltoDict = makeDelegatedToFrame(hiddableFrame)
    # deltoFrame.pack()
    # delfromFrame, delfromDict = makeDelegatedFromFrame(hiddableFrame)
    # delfromFrame.pack()
    # sentbyFrame, sentbyDict = makeSentByFrame(hiddableFrame)
    # sentbyFrame.pack()
    # cnFrame, cnDict = makeCommonNameFrame(hiddableFrame)
    # cnFrame.pack()
    # dirFrame, dirDict = makeDirFrame(hiddableFrame)
    # dirFrame.pack() 
    # languageFrame, languageDict = makeLanguageFrame(hiddableFrame)
    # languageFrame.pack()

    return attendeeFrame
