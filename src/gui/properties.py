from tkinter import ttk
from TkToolTip import ToolTip
import tkinter as tk
import tkcalendar as tkc
from datetime import datetime

from src.utils import findLangIdFromLangValue
from src.backend.properties import *
# from src.gui.parameters import *
# from src.gui.rrule import *

"""
- grid documentation: https://tkdocs.com/tutorial/grid.html

Some guidelines:
- the grid management has to be managed in the dedicated function for each property, so the caller just has to grid it
- each function must put in the valueHolder["getValue"] a lambda function that returns the property object, None if there is an error
"""

def makeAttachmentFrame(root: tk.Frame, valueHolder: dict) -> tk.Frame :
    """
    create a frame for attachment property

    Params:
    ------
    - root: tk.Frame
        frame in which the newly created frame will be contained
    - valueHolder: dict
        dictionnary that will hold the attachment infos

    Returns:
    -------
    - tk.Frame: the newly created attachment frame
    """
    frame = tk.Frame(root)
    frame.rowconfigure(0, weight=0)
    # label place
    frame.columnconfigure(0, weight=0)
    # value place
    frame.columnconfigure(1, weight=1)
    # tooltip place
    frame.columnconfigure(2, weight=0)

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
    def getAttachment():
        return Attachement(entry.get(), None, None, None)
    valueHolder["getValue"] = getAttachment

    return frame

def makeCategoriesFrame(root: tk.Frame, valueHolder: dict, configuration: dict) -> tk.Frame :
    """
    create a frame for categories property

    Params:
    -------
    - root: tk.Frame
        parent frame
    - valueHolder: dict
        dictionary that will contain infos about categories values
    - configuration: dict
        dictionary containing default values for user choices

    Returns:
    --------
    - tk.Frame: newly created frame (still need to be grid)
    """
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
    def getCategories():
        return Categories([listbox.get(index) for index in listbox.curselection()])
    valueHolder["getValue"] = getCategories

    entry = tk.StringVar()
    entryWidget = ttk.Entry(hiddableFrame, textvariable=entry)
    entryWidget.grid(row=0, column=1, columnspan=2, sticky=[tk.W, tk.E])
    # let the user add a new category for this particular component
    def add():
        value = entry.get()
        if (value and value not in listbox.get(0, tk.END)):
            listbox.insert(listbox.size(), value)
        # the listbox height resize dynamically
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
        # the listbox height resize dynamically
        listbox.config(height=min(configuration["height"], listbox.size()))
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

# FIXME: once a choice is done, the text is blue highlighted, need to be removed
def makeClassificationFrame(root: tk.Frame, valueHolder: dict, configuration: dict) -> tk.Frame:
    """
    create a frame for classification property

    Params:
    -------
    - root: tk.Frame
        parent frame
    - valueHolder: dict
        dictionary that will contain infos about classification values
    - configuration: dict
        dictionary containing default values for user choice

    Returns:
    --------
    - tk.Frame: newly created frame (still need to be grid)
    """
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
    userChoice = tk.StringVar(value="")
    combobox = ttk.Combobox(
        hiddableFrame,
        textvariable=userChoice,
        values=configuration["choices"],
        state=["readonly"],
        height=min(configuration["height"], len(configuration["choices"])),
    )
    # avoid selected item to be blue highlighted
    combobox.bind('<<ComboboxSelected>>', lambda e: e.widget.selection_clear())
    combobox.grid(row=0, rowspan=3, column=0, sticky=[tk.N])
    def getClassification():
        return Classification(combobox.get())
    valueHolder["getValue"] = getClassification

    entry = tk.StringVar()
    entryWidget = ttk.Entry(hiddableFrame, textvariable=entry)
    entryWidget.grid(row=0, column=1, columnspan=2, sticky=[tk.W, tk.E])
    # let the user add a new classification for this particular component
    def add():
        value = entry.get()
        if (value and value not in combobox["values"]):
            newChoices = list(combobox["values"])
            newChoices.append(value)
            combobox["values"] = newChoices
            combobox.set(value)
            # the listbox height resize dynamically
            combobox.config(height=min(configuration["height"], len(combobox["values"])))
        entry.set(value="")
    addButton = tk.Button(hiddableFrame, text="Add", command=add)
    addButton.grid(row=1, column=1, sticky=[tk.W, tk.E])

    # let the user add a new classification in the configuration
    def addToConfig():
        value = entry.get()
        if (value and value not in configuration["choices"]):
            configuration["choices"].append(value)
        add()
        entry.set(value="")
    addConfigButton = tk.Button(hiddableFrame, text="Add to configuration", command=addToConfig)
    addConfigButton.grid(row=1, column=2, sticky=[tk.W, tk.E])

    # let the user remove a classification from the configuration
    def removeFromConfig():
        selection = combobox.get()
        if (selection and selection in configuration["choices"]):
            configuration["choices"].remove(selection)
        remove()
    removeConfigButton = tk.Button(hiddableFrame, text="Remove from configuration", command=removeFromConfig)
    removeConfigButton.grid(row=2, column=2, sticky=[tk.W, tk.E])

    # let the user remove a classification for this particular component
    def remove():
        selection = combobox.get()
        if (selection and selection in combobox["values"]):
            newChoices = list(combobox["values"])
            newChoices.remove(selection)
            combobox["values"] = newChoices
            combobox.set(combobox["values"][0])
            # the listbox height resize dynamically
            combobox.config(height=min(configuration["height"], len(combobox["values"])))
    removeButton = tk.Button(hiddableFrame, text="Remove", command=remove)
    removeButton.grid(row=2, column=1, sticky=[tk.W, tk.E])

    # check button logic
    state = tk.BooleanVar(value=False)
    valueHolder["state"] = state
    def displayChoicesFrame():
        if (state.get()):
            hiddableFrame.grid()
            checkbutton.config(text="Classification: ")
            pass
        else:
            hiddableFrame.grid_remove()
            checkbutton.config(text="Classification ?")
            pass
    checkbutton = ttk.Checkbutton(frame, text="Classification ? ", variable=state, offvalue=False, onvalue=True, command=displayChoicesFrame)
    checkbutton.grid(row=0, column=0, sticky=[tk.N])

    return frame

# FIXME: when resized, the second column could disappear below the first one
# TODO: add a text inside showing if it's a description or comment component
def makeCommentOrDescriptionFrame(root: tk.Frame, valueHolder: dict, _type: str, configuration: [dict]) -> tk.Frame:
    if (_type not in ["comment", "description"]):
        return None

    frame = tk.Frame(root)
    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)

    textWidget = tk.Text(frame)
    textWidget.grid(row=0, rowspan=2, column=0)

    altrepEntry = ttk.Entry(frame)
    altrepEntry.grid(row=0, column=1)

    languageCombobox = ttk.Combobox(
        frame,
        values=[value[1] for value in configuration["choices"]],
        height=10,
        state=["readonly"]
    )
    # avoid selected item to be blue highlighted
    languageCombobox.bind('<<ComboboxSelected>>', lambda e: e.widget.selection_clear())
    languageCombobox.grid(row=1, column=1)

    def getCommentOrDescription():
        text = textWidget.get('1.0', 'end').strip()
        language = None
        for [key, value] in configuration["choices"]:
            if (value == languageCombobox.get()):
                language = key
                break
        altrep = altrepEntry.get()
        truc = None
        if (_type == "comment"):
            truc = Comment(text, altrep, language)
        else:
            truc = Description(text, altrep, language)
        return truc
    valueHolder["getValue"] = getCommentOrDescription

    return frame

def makeGeoFrame(root: tk.Frame, valueHolder: dict) -> tk.Frame:
    frame = tk.Frame(root)
    for i in range(2):
        frame.rowconfigure(i, weight=0)
    for i in range(3):
        frame.columnconfigure(i, weight=0)

    latVar = tk.StringVar(value=None)
    latSpinbox = ttk.Spinbox(frame, from_=-90.000000, to=90.000000, wrap=True, increment=0.000001, textvariable=latVar)
    latSpinbox.grid(row=1, column=0)
    latSpinbox.grid_remove()
    sep = tk.Label(frame, text=" ; ")
    sep.grid(row=1, column=1)
    sep.grid_remove()
    longVar = tk.StringVar(value=None)
    longSpinbox = ttk.Spinbox(frame, from_=-180.000000, to=180.000000, wrap=True, increment=0.000001, textvariable=longVar)
    longSpinbox.grid(row=1, column=3)
    longSpinbox.grid_remove()

    
    state = tk.BooleanVar(value=False)
    def toggleGeo():
        if (state.get()):
            latSpinbox.grid()
            sep.grid()
            longSpinbox.grid()
        else:
            latSpinbox.grid_remove()
            sep.grid_remove()
            longSpinbox.grid_remove()
            pass
    checkbutton = ttk.Checkbutton(frame, text="Geographical position", variable=state, offvalue=False, onvalue=True, command=toggleGeo)
    checkbutton.grid(row=0, column=0, columnspan=3, sticky=[tk.W, tk.E])

    def getGeo():
        return Geo(int(latVar.get()), int(longVar.get()))
    valueHolder["getValue"] = getGeo

    return frame

def makeLocationFrame(root: tk.Frame, valueHolder: dict, configuration: dict) -> tk.Frame:
    frame = tk.Frame(root)
    frame.rowconfigure(0, weight=0)
    frame.rowconfigure(1, weight=0)
    frame.columnconfigure(0, weight=0)
    frame.columnconfigure(1, weight=0)
    frame.columnconfigure(2, weight=0)

    state = tk.BooleanVar(value = False)
    label = tk.Label(frame, text="Location")
    label.grid(row=0, rowspan=2, column=0)
    entry = tk.StringVar()
    entryWidget = tk.Entry(frame, textvariable=entry)
    entryWidget.grid(row=0, rowspan=2, column=1, sticky=[tk.N, tk.S])

    altrep = tk.StringVar()
    altrepEntry = ttk.Entry(frame, textvariable=altrep)
    altrepEntry.grid(row=0, column=2, sticky=[tk.W, tk.E])
    altrepEntry.grid_remove()

    languageCombobox = ttk.Combobox(
        frame,
        values=[value[1] for value in configuration["choices"]],
        height=10,
        state=["readonly"]
    )
    # avoid the selected item to be blue highlighted
    languageCombobox.bind('<<ComboboxSelected>>', lambda e: e.widget.selection_clear())
    languageCombobox.grid(row=1, column=2)
    languageCombobox.grid_remove()
    

    def toggleParameters(event):
        tmp = state.get()
        if (tmp):
            altrepEntry.grid()
            languageCombobox.grid()
        else:
            altrepEntry.grid_remove()
            languageCombobox.grid_remove()
        state.set(not tmp)
    label.bind('<Double-1>', toggleParameters)

    def getLocation():
        if (not entry.get()):
            return None
        language = None
        altrepValue = None
        if (state.get()):
            for [key, value] in configuration["choices"]:
                if (value == languageCombobox.get()):
                    language = key
                    break
        return Location(entry.get(), altrepValue, language)
    valueHolder["getValue"] = getLocation

    return frame

# FIXME: make it comply with the other functions
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

def makePriorityFrame(root: tk.Frame, valueHolder: dict, configuration: dict) -> tk.Frame:
    frame = tk.Frame(root)
    frame.rowconfigure(0, weight=0)
    frame.columnconfigure(0, weight=0)
    frame.columnconfigure(1, weight=0)

    tk.Label(frame, text="Priority level: ").grid(row=0, column=0)
    priority = tk.StringVar(value="")
    spinbox = ttk.Spinbox(
        frame,
        from_=configuration["min"],
        to=configuration["max"],
        increment=configuration["step"],
        textvariable=priority,
        wrap=True
    )
    spinbox.set(configuration["default"])
    spinbox.grid(row=0, column=1)

    def getPriority():
        if (not priority.get()):
            return None
        return Priority(int(priority.get()))
    valueHolder["getValue"] = getPriority

    return frame

# TODO: flemme la tout de suite
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

def makeStatusFrame(root: tk.Frame, valueHolder: dict, componentType: str, configuration: dict) -> tk.Frame:
    frame = tk.Frame(root)
    frame.rowconfigure(0, weight=0)
    frame.rowconfigure(1, weight=0)
    frame.columnconfigure(0, weight=0)

    label = ttk.Label(frame, text="Status ?")
    label.grid(row=0, column=0)
    state = tk.BooleanVar(value=False)
    def showStatus(event):
        tmp = not state.get()
        if (tmp):
            statusCombobox.grid(row=1, column=0)
        else:
            statusCombobox.grid_remove()
        state.set(tmp)
    label.bind('<Double-1>', showStatus)

    value = tk.StringVar(value="")
    statusCombobox = ttk.Combobox(
        frame,
        values=configuration[f"{componentType}"],
        state=["readonly"],
        textvariable=value,
    )
    # avoid the selected item to be blue highlighted
    combobox.bind('<<ComboboxSelected>>', lambda e: e.widget.selection_clear())
    statusCombobox.grid(row=0, column=0)
    statusCombobox.grid_remove()

    def getStatus():
        if (not state.get() or not statusCombobox.get()):
            return None
        else:
            return Status(statusCombobox.get())
    valueHolder["getValue"] = getStatus

    return frame

def makeSummaryFrame(root: tk.Frame, valueHolder: dict, configuration: dict) -> tk.Frame:
    frame = tk.Frame(root)
    frame.rowconfigure(0, weight=0)
    frame.rowconfigure(1, weight=0)
    frame.columnconfigure(0, weight=0)
    frame.columnconfigure(1, weight=0)

    label = ttk.Label(frame, text="Title: ")
    label.grid(row=0, column=0)

    title = tk.StringVar()
    summaryEntry = ttk.Entry(frame, textvariable=title)
    summaryEntry.grid(row=0, column=1, sticky="nsew")

    altrep = tk.StringVar()
    altrepEntry = ttk.Entry(frame, textvariable=altrep)
    altrepEntry.grid(row=1, column=0, sticky=[tk.W, tk.E])
    altrepEntry.grid_remove()

    languageCombobox = ttk.Combobox(
        frame,
        values=[value[1] for value in configuration["choices"]],
        height=10,
        state=["readonly"]
    )
    # avoid the selected item to be blue highlighted
    languageCombobox.bind('<<ComboboxSelected>>', lambda e: e.widget.selection_clear())
    languageCombobox.grid(row=1, column=1)
    languageCombobox.grid_remove()

    state = tk.BooleanVar(value=False)
    def toggleParameters(event):
        tmp = state.get()
        if (tmp):
            altrepEntry.grid()
            languageCombobox.grid()
        else:
            altrepEntry.grid_remove()
            languageCombobox.grid_remove()
        state.set(not tmp)
    label.bind('<Double-1>', toggleParameters)

    def getSummary():
        if (not title.get()):
            return None
        language = None
        altrepValue = None
        if (state.get()):
            for [key, value] in configuration["choices"]:
                if (value == languageCombobox.get()):
                    language = key
                    break
        return Summary(title.get(), altrepValue, language)
    valueHolder["getValue"] = getSummary
    # to be able to display the title in real time
    valueHolder["titleEntry"] = summaryEntry

    return frame

# TODO: put default value for start are now and for end its start + default duration
def makeDtFrame(root, typename: str, valueHolder: dict) -> tk.Frame:
    frame = tk.Frame(root)
    for i in range(2):
        frame.rowconfigure(i, weight=0)
    for i in range(3):
        frame.columnconfigure(i, weight=0)

    timestamp = datetime.now()

    labeltext = "From" if typename == "start" else "to"
    label = tk.Label(frame, text=labeltext)
    label.grid(row=0, column=0)

    dateEntry = tkc.DateEntry(
        frame,
        selectmode="day",
        date_pattern="y/mm/dd"
    )
    dateEntry.grid(row=0, column=1, columnspan=2)
    # line below is mandatroy: let the calendar be clickable even if there is a widget below it on the z-axis
    dateEntry._top_cal.lift()

    # check that user inpput for spinboxes are valid
    def validateSpinboxInputWhenKey(max, text):
        if (not text):
            return True
        if (text and len(text) > 2):
            return False
        try:
            tmp = int(text)
            return tmp >= 0 and tmp <= max
        except:
            return False

    hour = tk.StringVar(value="0")
    hourSpinbox = ttk.Spinbox(
        frame,
        from_=0,
        to=23,
        increment=1,
        width=3,
        textvariable=hour,
        wrap=True,
        validate="key", # this line and the one below ensure that what is typed in the keyboard is a valid value
        validatecommand=(frame.register(lambda t: validateSpinboxInputWhenKey(23, t)), "%P")
    )
    hourSpinbox.grid(row=2, column=0)
    minute = tk.StringVar(value="0")
    minuteSpinbox = ttk.Spinbox(
        frame,
        from_=0,
        to=59,
        increment=1,
        width=3,
        textvariable=minute,
        wrap=True,
        validate="key",
        validatecommand=(frame.register(lambda t: validateSpinboxInputWhenKey(59, t)), "%P")
    )
    minuteSpinbox.grid(row=2, column=1)
    second = tk.StringVar(value="0")
    secondSpinbox = ttk.Spinbox(
        frame,
        from_=0,
        to=59,
        increment=1,
        width=3,
        textvariable=second,
        wrap=True,
        validate="key",
        validatecommand=(frame.register(lambda t: validateSpinboxInputWhenKey(59, t)), "%P")
    )
    secondSpinbox.grid(row=2, column=2)

    def getDT():
        return datetime(
            year=int(dateEntry.get_date().strftime("%Y")),
            month=int(dateEntry.get_date().strftime("%m")),
            day=int(dateEntry.get_date().strftime("%d")),
            hour=hour.get(),
            minute=minute.get(),
            second=second.get()
        )
    valueHolder["getValue"] = getDT

    return frame

# TODO
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

def makeTranspFrame(root: tk.Frame, valueHolder: dict, configuration: dict) -> tk.Frame:
    frame = tk.Frame(root)

    value = tk.StringVar(value=configuration["choices"][0])
    transpCombobox = ttk.Combobox(
        frame,
        values=configuration["choices"],
        state=["readonly"],
        textvariable=value
    )
    # avoid the selected item to be blue highlighted
    combobox.bind('<<ComboboxSelected>>', lambda e: e.widget.selection_clear())
    transpCombobox.grid()

    ToolTip(transpCombobox, msg="Tells if the event should block overlapping events")

    def getTransp():
        return Transparency(value.get())
    valueHolder["getValue"] = getTransp

    return frame

# TODO: work on how to use cal-addresses
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
        textvariable=value,
        state=["readonly"]
    )
    # avoid the selected item to be blue highlighted
    combobox.bind('<<ComboboxSelected>>', lambda e: e.widget.selection_clear())
    combobox.pack(side="right")

    return frame, value

# TODO: work on how to use cal-addresses
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

def makeURLFrame(root: tk.Frame, valueHolder: dict) -> tk.Frame:
    frame = tk.Frame(root)
    frame.rowconfigure(0, weight=0)
    frame.columnconfigure(0, weight=0)
    frame.columnconfigure(1, weight=0)

    tk.Label(frame, text="URL: ").grid(row=0, column=0)
    value = tk.StringVar(value="")
    entry = tk.Entry(frame, textvariable=value)
    entry.grid(row=0, column=1)

    def getURL():
        if not (entry.get()):
            return None
        return Url(entry.get())
    valueHolder["getValue"] = getURL

    return frame

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