from src.gui.imports import *
from TkToolTip import ToolTip
from src.backend.properties.descriptive import Attachment, Categories, Classification, Comment, Description, Geo, Location, Percent, Priority, Resources, Status, Summary
from src.gui.parameters import *

"""
NOTE: for every function
- frame is the main frame of the property, that's on the caller to grid it
- get<PropertyName>() let the dev call this function later, on component creation. Please ease this call by
    return the object only if everything is fine. Put the object instanciation in try catch scope to be able
    to log the error message if any (still need to be done)
- please put [Component {componentId}] at the beginning of every logs for simpler debugging
"""

# TODO: remake makePercentFrame
# TODO: use parameter frame functions in property frame functions
# TODO: put every property object creation in a try catch scope
# TODO: check that everything is logged well

def makeAttachmentFrame(root: tk.Frame, valueHolder: dict, componentId: uuid) -> tk.Frame :
    """
    create a frame for attachment property and a lambda function to get the attachment object

    Params:
    ------
    - root: tk.Frame
        frame in which the newly created frame will be contained
    - valueHolder: dict
        dictionnary that will hold a lambda function which returns the attachment object from the user input, None if any error occured
    - componentId: uuid
        ID of the parent component

    Returns:
    -------
    - tk.Frame: the newly created attachment frame (still needs to be grided)
    """
    frame = tk.Frame(root)
    # only entry widget needs to be resized on window resize
    frame.columnconfigure(1, weight=1)

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
        try:
            tmp = None
            if (entry.get()):
                tmp = Attachment(entry.get(), None, None, None)
            return tmp
        except:
            logging.warn(f"[Component {id_}] Failed to create attachement")
            return None
    valueHolder["getValue"] = getAttachment

    return frame

def makeCategoriesFrame(root: tk.Frame, valueHolder: dict, componentId: uuid) -> tk.Frame :
    """
    create a frame for categories property and a lambda function to get the Categories object

    Params:
    ------
    - root: tk.Frame
        frame in which the newly created frame will be contained
    - valueHolder: dict
        dictionnary that will hold a lambda function which returns the Categories object from the user input, None if any error occured
    - componentId: uuid
        ID of the parent component

    Returns:
    -------
    - tk.Frame: the newly created categories frame (still needs to be grided)
    """

    frame = tk.Frame(root)

    listbox = tk.Listbox(
        frame,
        selectmode="multiple",
        exportselection=False, # NOTE: don't remove: avoid listbox selection being vanished when focus on another widget
        height=min(configuration["categories"]["height"], len(configuration["categories"]["choices"]))
    )
    for i in range(len(configuration["categories"]["choices"])):
        listbox.insert(i, configuration["categories"]["choices"][i])
    listbox.grid(row=0, rowspan=3, column=0, sticky=[tk.N])

    def getCategories():
        selectedCategories = [listbox.get(index) for index in listbox.curselection()]
        if (selectedCategories == []):
            return None
        try:
            categories = Categories(selectedCategories)
            return categories
        except:
            logging.warn(f"[Component {componentId}] Unable to create categories")
            return None
    valueHolder["getValue"] = getCategories

    return frame

def makeClassificationFrame(root: tk.Frame, valueHolder: dict, componentId: uuid) -> tk.Frame:
    """
    create a frame for classification property and a lambda function to get the Classification object

    Params:
    ------
    - root: tk.Frame
        frame in which the newly created frame will be contained
    - valueHolder: dict
        dictionnary that will hold a lambda function which returns the Classification object from the user input, None if any error occured
    - componentId: uuid
        ID of the parent component

    Returns:
    -------
    - tk.Frame: the newly created classification frame (still needs to be grided)
    """

    # main frame
    frame = tk.Frame(root)

    # display all the categories
    placeholder = "Choose a classification"
    choice = tk.StringVar(value=placeholder)
    combobox = ttk.Combobox(
        frame,
        textvariable=choice,
        values=configuration["classification"]["choices"],
        state=["readonly"],
        height=min(configuration["classification"]["height"], len(configuration["classification"]["choices"])),
    )
    combobox.set(placeholder)
    # avoid selected item to be blue highlighted
    combobox.bind('<<ComboboxSelected>>', lambda e: e.widget.selection_clear())
    frame.columnconfigure(0, weight=1)
    combobox.grid(row=0, column=0, columnspan=2, sticky="nsew")

    def getClassification():
        value = combobox.get()
        if (not value):
            return None
        if (not value.strip() or value == placeholder):
            return None
        return Classification(value.strip())
    valueHolder["getValue"] = getClassification

    entryValue = tk.StringVar(value="")
    entry = ttk.Entry(frame, textvariable=entryValue)
    entry.grid(row=1, column=0, sticky="nsew")

    # let the user add a new classification for this particular component
    def add():
        value = entryValue.get()
        if (value and value not in combobox["values"] and value != placeholder):
            newChoices = list(combobox["values"])
            newChoices.append(value)
            combobox["values"] = newChoices
            # the listbox height resize dynamically
            combobox.config(height=min(configuration["classification"]["height"], len(combobox["values"])))
            choice.set(value=value)
            entryValue.set("") 
    addButton = tk.Button(frame, text="+", command=add)
    addButton.grid(row=1, column=1, sticky="nsew")

    return frame

# TODO: check if it works
# TODO: add logging
def makeCommentFrame(root: tk.Frame, valueHolder: dict, componentId: uuid) -> tk.Frame:
    """
    create a frame for comment property and a lambda function to get the Comment object with valueHolder["getValue"]()

    Params:
    ------
    - root: tk.Frame
        frame in which the newly created frame will be contained
    - valueHolder: dict
        dictionnary that will hold a lambda function which returns the Comment object from the user input, None if any error occured
    - componentId: uuid
        ID of the parent component

    Returns:
    -------
    - tk.Frame: the newly created comment frame (still needs to be grided)
    """

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
        values=[value[1] for value in configuration["language"]["choices"]],
        height=10,
        state=["readonly"]
    )
    # avoid selected item to be blue highlighted
    languageCombobox.bind('<<ComboboxSelected>>', lambda e: e.widget.selection_clear())
    languageCombobox.grid(row=1, column=1)

    def getComment():
        text = textWidget.get('1.0', 'end').strip()
        if (not text):
            return None

        language = None
        for [key, value] in configuration["language"]["choices"]:
            if (value == languageCombobox.get()):
                language = key
                break
        altrep = altrepEntry.get()
        truc = None
        truc = Comment(text, altrep, language)
        return truc
    valueHolder["getValue"] = getComment

    return frame

# FIXME: when resized, the second column could disappear below the first one
def makeDescriptionFrame(root: tk.Frame, valueHolder: dict, componentId: uuid) -> tk.Frame:
    """
    create a frame for description property and a lambda function to get the Description object with valueHolder["getValue"]()

    Params:
    ------
    - root: tk.Frame
        frame in which the newly created frame will be contained
    - valueHolder: dict
        dictionnary that will hold a lambda function which returns the Description object from the user input, None if any error occured
    - componentId: uuid
        ID of the parent component

    Returns:
    -------
    - tk.Frame: the newly created description frame (still needs to be grided)
    """

    frame = tk.Frame(root)
    # only description textbox needs to be resized on window resizing
    frame.rowconfigure(1, weight=1)
    frame.columnconfigure(1, weight=1)

    textWidget = tk.Text(frame)
    textWidget.grid(row=0, rowspan=2, column=0)

    altrepEntry = ttk.Entry(frame)
    altrepEntry.grid(row=0, column=1)

    languageCombobox = ttk.Combobox(
        frame,
        values=[value[1] for value in configuration["language"]["choices"]],
        height=10,
        state=["readonly"]
    )
    # avoid selected item to be blue highlighted
    languageCombobox.bind('<<ComboboxSelected>>', lambda e: e.widget.selection_clear())
    languageCombobox.grid(row=1, column=1)

    def getDescription():
        text = textWidget.get('1.0', 'end').strip()
        if (not text):
            return None

        language = None
        text = text.strip()
        for [key, value] in configuration["language"]["choices"]:
            if (value == languageCombobox.get()):
                language = key
                break
        altrep = altrepEntry.get()
        description = None
        description = Description(text, altrep, language)
        return description
    valueHolder["getValue"] = getDescription

    return frame

def makeGeoFrame(root: tk.Frame, valueHolder: dict) -> tk.Frame:
    """
    create a frame for geo property and a lambda function to get the Geo object with valueHolder["getValue"]()

    Params:
    ------
    - root: tk.Frame
        frame in which the newly created frame will be contained
    - valueHolder: dict
        dictionnary that will hold a lambda function which returns the Geo object from the user input, None if any error occured
    - componentId: uuid
        ID of the parent component

    Returns:
    -------
    - tk.Frame: the newly created geo frame (still needs to be grided)
    """

    frame = tk.Frame(root)

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
        if (not state.get()):
            return None
        
        try:
            lat = int(latVar.get())
            long = int(longVar.get())
            tmp = Geo(lat, long)
            logging.debug(f"Geographical location successfully created")
            return tmp
        except:
            logging.error(f"Unable to make a geographical coordinates with {latVar.get()} and {longVar.get()}")
    valueHolder["getValue"] = getGeo

    return frame

def makeLocationFrame(root: tk.Frame, valueHolder: dict, componentId: uuid) -> tk.Frame:
    """
    create a frame for location property and a lambda function to get the Location object with valueHolder["getValue"]()

    Params:
    ------
    - root: tk.Frame
        frame in which the newly created frame will be contained
    - valueHolder: dict
        dictionnary that will hold a lambda function which returns the Location object from the user input, None if any error occured
    - componentId: uuid
        ID of the parent component

    Returns:
    -------
    - tk.Frame: the newly created location frame (still needs to be grided)
    """

    frame = tk.Frame(root)
    frame.columnconfigure(1, weight=1)

    label = tk.Label(frame, text="Location: ")
    label.grid(row=0, column=0)

    entry = tk.Entry(frame)
    entry.grid(row=0, column=1, stick="nsew")

    # hold the information if parameters frame exist and are displayed
    state = tk.BooleanVar(value=False)
    languageDict = {}
    languageFrame = None
    altrepDict = {}
    altrepFrame = None

    def toggleParameterFrame(event):
        # nonlocal let the two frames be created only if needed
        nonlocal languageFrame
        nonlocal altrepFrame
        # reverse the boolean value if label is clicked
        actual = not state.get()
        if (actual):
            if (not languageFrame):
                altrepFrame = makeAlternativeRepresentationFrame(frame, altrepDict, "location")
                altrepFrame.grid(row=1, column=1, sticky="nsew")
                languageFrame = makeLanguageFrame(frame, languageDict)
                languageFrame.grid(row=2, column=1, sticky="nsew")
            altrepFrame.grid()
            languageFrame.grid()
        else:
            altrepFrame.grid_remove()
            languageFrame.grid_remove()
        state.set(actual)
    label.bind('<Double-1>', toggleParameterFrame)

    def getLocation():
        if (not entry.get()):
            return None
        if (not entry.get().strip()):
            return None
        value = entry.get().strip()
        altrep = altrepDict["getValue"]() if state.get() else None
        language = languageDict["getValue"]() if state.get() else None
        return Location(value, altrep, language)
    valueHolder["getValue"] = getLocation

    return frame

# FIXME: make it comply with the other functions
def makePercentFrame(root: tk.Frame, valueHolder: dict, componentId: uuid) -> tk.Frame :
    """
    create a frame for percent property and a lambda function to get the Percent object with valueHolder["getValue"]()

    Params:
    ------
    - root: tk.Frame
        frame in which the newly created frame will be contained
    - valueHolder: dict
        dictionnary that will hold a lambda function which returns the Percent object from the user input, None if any error occured
    - componentId: uuid
        ID of the parent component

    Returns:
    -------
    - tk.Frame: the newly created percent frame (still needs to be grided)
    """

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

    return frame

def makePriorityFrame(root: tk.Frame, valueHolder: dict, componentId: uuid) -> tk.Frame:
    """
    create a frame for priority property and a lambda function to get the Priority object with valueHolder["getValue"]()

    Params:
    ------
    - root: tk.Frame
        frame in which the newly created frame will be contained
    - valueHolder: dict
        dictionnary that will hold a lambda function which returns the Priority object from the user input, None if any error occured
    - componentId: uuid
        ID of the parent component

    Returns:
    -------
    - tk.Frame: the newly created priority frame (still needs to be grided)
    """

    frame = tk.Frame(root)

    tk.Label(frame, text="Priority level: ").grid(row=0, column=0)
    priority = tk.StringVar(value="")
    spinbox = ttk.Spinbox(
        frame,
        from_=configuration["priority"]["min"],
        to=configuration["priority"]["max"],
        increment=configuration["priority"]["step"],
        textvariable=priority,
        wrap=True
    )
    spinbox.set(configuration["priority"]["default"])
    spinbox.grid(row=0, column=1)

    def getPriority():
        if (not priority.get()):
            return None
        try:
            tmp = Priority(int(priority.get()))
            # logging.debug(f"priority successfully created")
            return tmp
        except:
            logging.error(f"[Component {componentId}] Unable to create priority")
            return None
    valueHolder["getValue"] = getPriority

    return frame

def makeResourceFrame(root: tk.Frame, valueHolder: dict, componentId: uuid) -> tk.Frame:
    """
    create a frame for resources property and a lambda function to get the Resources object with valueHolder["getValue"]()

    Params:
    ------
    - root: tk.Frame
        frame in which the newly created frame will be contained
    - valueHolder: dict
        dictionnary that will hold a lambda function which returns the Resources object from the user input, None if any error occured
    - componentId: uuid
        ID of the parent component

    Returns:
    -------
    - tk.Frame: the newly created resources frame (still needs to be grided)
    """

    frame = ttk.LabelFrame(root, text="Required resources")
    frame.columnconfigure(0, weight=1)

    listbox = tk.Listbox(
        frame,
        selectmode="multiple",
        height=min(configuration["resources"]["height"], len(configuration["resources"]["choices"])),
        width=max([len(item) for item in configuration["resources"]["choices"]])
    )
    for i in range(len(configuration["resources"]["choices"])):
        listbox.insert(i, configuration["resources"]["choices"][i])
    listbox.grid(row=0, column=0, sticky=(tk.N, tk.S))

    scrollbar = ttk.Scrollbar(
        frame,
        orient=tk.VERTICAL,
        command=listbox.yview  # Link scrollbar to listbox
    )
    scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    listbox["yscrollcommand"] = scrollbar.set

    def getResources():
        tmpList = [listbox.get(index) for index in listbox.curselection()]
        if (tmpList == []):
            return None
        try:
            resources = Resources(tmpList, None, None)
            return resources
        except:
            raise Exception(f"[Component {componentId}] Unable to make the resources property")
    valueHolder["getValue"] = getResources

    return frame

def makeStatusFrame(root: tk.Frame, valueHolder: dict, componentType: str) -> tk.Frame:
    """
    create a frame for status property and a lambda function to get the Status object with valueHolder["getValue"]()

    Params:
    ------
    - root: tk.Frame
        frame in which the newly created frame will be contained
    - valueHolder: dict
        dictionnary that will hold a lambda function which returns the Status object from the user input, None if any error occured
    - componentId: uuid
        ID of the parent component

    Returns:
    -------
    - tk.Frame: the newly created status frame (still needs to be grided)
    """

    frame = tk.Frame(root)

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
        values=configuration["status"][f"{componentType}"],
        state=["readonly"],
        textvariable=value,
    )
    # avoid the selected item to be blue highlighted
    combobox.bind('<<ComboboxSelected>>', lambda e: e.widget.selection_clear())
    statusCombobox.grid(row=0, column=0)
    statusCombobox.grid_remove()

    def getStatus():
        if (not state.get() or not value.get()):
            return None
        try:
            tmp = Status(value.get())
            logging.debug(f"Status successfully created") 
            return tmp
        except:
            logging.debug(f"Unable to create {state.get()} status")
            return None
    valueHolder["getValue"] = getStatus

    return frame

def makeSummaryFrame(root: tk.Frame, valueHolder: dict, componentId: uuid) -> tk.Frame:
    """
    create a frame for summary property and a lambda function to get the Summary object with valueHolder["getValue"]()

    Params:
    ------
    - root: tk.Frame
        frame in which the newly created frame will be contained
    - valueHolder: dict
        dictionnary that will hold a lambda function which returns the Summary object from the user input, None if any error occured
    - componentId: uuid
        ID of the parent component

    Returns:
    -------
    - tk.Frame: the newly created summary frame (still needs to be grided)
    """

    frame = tk.Frame(root)
    frame.columnconfigure(1, weight=1)

    label = ttk.Label(frame, text="Title: ")
    label.grid(row=0, column=0)

    entry = ttk.Entry(frame)
    entry.grid(row=0, column=1, sticky="nsew")

    # hold the information if parameters frame exist and are displayed
    state = tk.BooleanVar(value=False)
    languageDict = {}
    languageFrame = None
    altrepDict = {}
    altrepFrame = None

    def toggleParameterFrame(event):
        # nonlocal let the two frames be created only if needed
        nonlocal languageFrame
        nonlocal altrepFrame
        # reverse the boolean value if label is clicked
        actual = not state.get()
        if (actual):
            if (not languageFrame):
                altrepFrame = makeAlternativeRepresentationFrame(frame, altrepDict, "title")
                altrepFrame.grid(row=1, column=1, sticky="nsew")
                languageFrame = makeLanguageFrame(frame, languageDict)
                languageFrame.grid(row=2, column=1, sticky="nsew")
            altrepFrame.grid()
            languageFrame.grid()
        else:
            altrepFrame.grid_remove()
            languageFrame.grid_remove()
        state.set(actual)
    label.bind('<Double-1>', toggleParameterFrame)

    def getSummary():
        if (not entry.get()):
            return None
        if (not entry.get().strip()):
            return None
        value = entry.get().strip()
        altrep = altrepDict["getValue"]() if state.get() else None
        language = languageDict["getValue"]() if state.get() else None
        return Summary(value, altrep, language)
    valueHolder["getValue"] = getSummary
    # to be able to display the title in real time
    valueHolder["titleEntry"] = entry

    return frame
