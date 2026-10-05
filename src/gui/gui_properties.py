from tkinter import ttk
import tkinter as tk
from src.gui.gui_parameters import *
import tkcalendar as tkc
from datetime import datetime
from utils import configuration, logging

# NOTE: put the user input part in a hiddable frame iff the frame is optional for all the types of event it can appears

def makeAttachmentFrame(masterFrame, configuration):
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

def makeCategoriesFrame(masterFrame, configuration):
    categoriesFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(categoriesFrame)

    userFrame = tk.Frame(hiddableFrame)

    listbox = tk.Listbox(
        userFrame,
        selectmode="multiple",
        height=min(configuration["categories"]["height"], len(configuration["categories"]["choices"]))
    )
    for i in range(len(configuration["categories"]["choices"])):
        listbox.insert(i, configuration["categories"]["choices"][i])
    listbox.pack()
    userInput = tk.Entry(userFrame)
    userInput.pack()

    languageFrame, languageInput = makeLanguageFrame(hiddableFrame, configuration)
    languageFrame.pack(side="bottom")
    userFrame.pack(side="left")

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
    def toggleHiddableFrame():
        if (buttonState.get()):
            hiddableFrame.pack()
        else:
            hiddableFrame.pack_forget()
    checkbutton = tk.Checkbutton(categoriesFrame, text="Categories ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    checkbutton.pack()

    categoriesDict = {
        "state": buttonState,
        "listbox": listbox,
        "language": languageInput
    }

    return categoriesFrame, categoriesDict

def makeClassificationFrame(masterFrame, configuration):
    classificationFrame = tk.Frame(masterFrame)

    value = tk.StringVar(value="")
    hiddableFrame = tk.Frame(classificationFrame)
    combobox = ttk.Combobox(
        hiddableFrame,
        values=configuration["classification"]["choices"],
        state="readonly",
        textvariable=value
    )
    combobox.pack()

    buttonState = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (buttonState.get()):
            checkbutton.config(text="Classification : ")
            hiddableFrame.pack(side="right")
        else:
            checkbutton.config(text="Classification ? ")
            hiddableFrame.pack_forget()
    checkbutton = tk.Checkbutton(classificationFrame, text="Classification ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    checkbutton.pack(side="left")
    
    classificationDict = {
        "state": buttonState,
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

    altrepFrame, altrepInput = makeAlternativeRepresentationFrame(hiddableFrame, configuration)
    altrepFrame.pack()

    languageFrame, languageInput = makeLanguageFrame(hiddableFrame, configuration)
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

def makeDescriptionFrame(masterFrame, configuration):
    descriptionFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(descriptionFrame)
    descriptionText = tk.Text(hiddableFrame)
    descriptionText.config(
        height=configuration["description"]["height"],
        width=configuration["description"]["width"]
    )
    descriptionText.pack()

    altrepFrame, altrepInput = makeAlternativeRepresentationFrame(hiddableFrame, configuration)
    altrepFrame.pack()

    languageFrame, languageInput = makeLanguageFrame(hiddableFrame, configuration)
    languageFrame.pack()

    buttonState = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (buttonState.get()):
            checkbutton.config(text="Description : ")
            hiddableFrame.pack()
        else:
            checkbutton.config(text="Description ? ")
            hiddableFrame.pack_forget()
    checkbutton = tk.Checkbutton(descriptionFrame, text="Description ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    checkbutton.pack()

    descriptionDict = {
        "state": buttonState,
        "value": descriptionText,
        "altrep": altrepInput,
        "language": languageInput
    }

    return descriptionFrame, descriptionDict

def makeGeoFrame(masterFrame, configuration):
    geoFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(geoFrame)
    latVar = tk.StringVar(value="")
    latSpinbox = ttk.Spinbox(hiddableFrame, from_=-90.000000, to=90.000000, wrap=True, increment=0.000001, textvariable=latVar)
    latSpinbox.pack(side="right")
    tk.Label(hiddableFrame, text=" ; ").pack(side="right")
    longVar = tk.StringVar(value="")
    longSpinbox = ttk.Spinbox(hiddableFrame, from_=-180.000000, to=180.000000, wrap=True, increment=0.000001, textvariable=longVar)
    longSpinbox.pack(side="right")

    buttonState = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (buttonState.get()):
            checkbutton.config(text="Geographic position : ")
            hiddableFrame.pack(side="right")
        else:
            checkbutton.config(text="Geographic position ? ")
            hiddableFrame.pack_forget()
    checkbutton = tk.Checkbutton(geoFrame, text="Geographic position ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    checkbutton.pack(side="left")

    geoDict = {
        "state": buttonState,
        "lat": latVar,
        "long": longVar
    }

    return geoFrame, geoDict

def makeLocationFrame(masterFrame, configuration):
    locationFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(locationFrame)
    locationText = tk.Text(hiddableFrame)
    locationText.config(
        height=configuration["location"]["height"],
        width=configuration["location"]["width"]
    )
    locationText.pack()

    altrepFrame, altrepInput = makeAlternativeRepresentationFrame(hiddableFrame, configuration)
    altrepFrame.pack()

    languageFrame, languageInput = makeLanguageFrame(hiddableFrame, configuration)
    languageFrame.pack()

    buttonState = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (buttonState.get()):
            checkbutton.config(text="Location : ")
            hiddableFrame.pack()
        else:
            checkbutton.config(text="Location ? ")
            hiddableFrame.pack_forget()
    checkbutton = tk.Checkbutton(locationFrame, text="Location ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    checkbutton.pack()

    locationDict = {
        "state": buttonState,
        "value": locationText,
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

    hiddableFrame = tk.Frame(priorityFrame)
    priorityVar = tk.StringVar(value="")
    latSpinbox = ttk.Spinbox(hiddableFrame, from_=0, to=9, increment=1, textvariable=priorityVar)
    latSpinbox.pack(side="right")

    buttonState = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (buttonState.get()):
            checkbutton.config(text="Priority level : ")
            hiddableFrame.pack(side="right")
        else:
            checkbutton.config(text="Priority level ? ")
            hiddableFrame.pack_forget()
    checkbutton = tk.Checkbutton(priorityFrame, text="Priority level ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    checkbutton.pack(side="left")

    priorityDict = {
        "state": buttonState,
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

    altrepFrame, altrepInput = makeAlternativeRepresentationFrame(hiddableFrame, configuration)
    altrepFrame.pack()

    languageFrame, languageInput = makeLanguageFrame(hiddableFrame, configuration)
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

def makeDtFrame(masterFrame, configuration, typename: str):
    # typename is the name of the type of the datime
    if (typename not in ["completed", "end", "due", "start"]):
        return None, None

    dtFrame = tk.Frame(masterFrame)

    today = datetime.now()
    hiddableFrame = tk.Frame(dtFrame)
    dateEntry = tkc.DateEntry(
        hiddableFrame,
        selectmode="day",
        date_pattern="y/mm/dd"
    )
    dateEntry.pack(side="left")

    buttonState = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (buttonState.get()):
            checkbutton.config(text=configuration[f"dt{typename}"]["checkedText"])
            hiddableFrame.pack(side="right")
        else:
            checkbutton.config(text=configuration[f"dt{typename}"]["uncheckedText"])
            hiddableFrame.pack_forget()
    checkbutton = tk.Checkbutton(dtFrame, text=configuration[f"dt{typename}"]["uncheckedText"], variable=buttonState, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    checkbutton.pack(side="left")

    timeFrame = tk.Frame(hiddableFrame)
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

    timebuttonState = tk.BooleanVar(value=configuration[f"dt{typename}"]["datetime-default"])
    def toggleHiddableTimeFrame():
        if (timebuttonState.get()):
            timecheckbutton.config(text=" at ")
            timeFrame.pack(side="right")
        else:
            timecheckbutton.config(text="Time ? ")
            timeFrame.pack_forget()
    timecheckbutton = tk.Checkbutton(hiddableFrame, text="Time ? ", variable=timebuttonState, offvalue=False, onvalue=True, command=toggleHiddableTimeFrame)
    timecheckbutton.pack(side="left")
    if (timebuttonState.get()):
        timecheckbutton.config(text=" at ")
        timeFrame.pack(side="right")

    dtDict = {
        "date-status": buttonState,
        "time-status": timebuttonState,
        "date": dateEntry,
        "time": timebuttonState,
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

def makeTranspFrame(masterFrame, configuration):
    transpFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(transpFrame)
    value = tk.StringVar(value="")
    transpCombobox = ttk.Combobox(
        hiddableFrame,
        values=configuration["transparency"]["choices"],
        state="readonly",
        textvariable=value
    )
    transpCombobox.pack()

    buttonState = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (buttonState.get()):
            hiddableFrame.pack(side="right")
        else:
            hiddableFrame.pack_forget()
    checkbutton = tk.Checkbutton(transpFrame, text="Transparency", variable=buttonState, onvalue=True, offvalue=False, command=toggleHiddableFrame)
    checkbutton.pack(side="left")

    transpDict = {
        "state": buttonState,
        "value": value
    }

    return transpFrame, transpDict

def makeAttendeeFrame(masterFrame, configuration, eventType: str):
    attendeeFrame = tk.Frame(masterFrame)

    userFrame = tk.Frame(attendeeFrame)
    value = tk.StringVar(value="")
    userInput = tk.Entry(attendeeFrame, textvariable=value)
    userInput.pack()

    hiddableFrame = tk.Frame(userFrame)
    cutypeFrame, cutypeDict = makeCutypeFrame(hiddableFrame, configuration)
    cutypeFrame.pack()
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
    # languageFrame, languageDict = makeLanguageFrame(hiddableFrame, configuration)
    # languageFrame.pack()

    state = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (state.get()):
            hiddableFrame.pack(side="right")
            button.config(text="Details : ")
        else:
            hiddableFrame.pack_forget()
            button.config(text="Details ? ")
    button = tk.Checkbutton(attendeeFrame, text="Details ? ", variable=state, onvalue=True, offvalue=False, command=toggleHiddableFrame)
    button.pack(side="left")

    return attendeeFrame