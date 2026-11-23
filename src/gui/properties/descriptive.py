from src.gui.imports import *
from TkToolTip import ToolTip
from src.backend.properties.descriptive import Attachment, Categories, Classification, Comment, Description, Geo, Location, Percent, Priority, Resources, Status, Summary

def makeAttachmentFrame(root: tk.Frame, valueHolder: dict, componentId: uuid) -> tk.Frame :
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
        try:
            tmp = None
            if (entry.get()):
                tmp = Attachment(entry.get(), None, None, None)
                # logging.debug(f"{entry.get()} attachment successfully created")
            return tmp
        except:
            logging.warn(f"[Component {id_}] Failed to create attachement")
            return None
    valueHolder["getValue"] = getAttachment

    return frame

# TODO: make it work
def makeCategoriesFrame(root: tk.Frame, valueHolder: dict, componentId: uuid) -> tk.Frame :
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

    # display all the categories
    listbox = tk.Listbox(
        frame,
        selectmode="multiple",
        exportselection=False,
        height=min(configuration["categories"]["height"], len(configuration["categories"]["choices"]))
    )
    for i in range(len(configuration["categories"]["choices"])):
        listbox.insert(i, configuration["categories"]["choices"][i])
    listbox.grid(row=0, rowspan=3, column=0, sticky=[tk.N])

    def _trace(name=None):
        print(f"sel={listbox.curselection()} size={listbox.size()}")
    listbox.bind("<<ListboxSelect>>", lambda e: _trace())

    def getCategories():
        tmpList = [listbox.get(index) for index in listbox.curselection()]
        if (tmpList == []):
            return None
        try:
            tmp = Categories(tmpList)
            # logging.debug("Categories successfully created")
            return tmp
        except:
            logging.warn(f"[Component {componentId}] Unable to create categories")
            return None
    valueHolder["getValue"] = getCategories

    return frame

def makeClassificationFrame(root: tk.Frame, valueHolder: dict, componentId) -> tk.Frame:
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
        values=configuration["classification"]["choices"],
        state=["readonly"],
        height=min(configuration["classification"]["height"], len(configuration["classification"]["choices"])),
    )
    # avoid selected item to be blue highlighted
    combobox.bind('<<ComboboxSelected>>', lambda e: e.widget.selection_clear())
    combobox.grid(row=0, rowspan=3, column=0, sticky=[tk.N])
    def getClassification():
        try:
            tmp = None
            if (userChoice.get()):
                tmp = Classification(userChoice.get())
                # logging.debug(f"User choosed {userChoice.get()} classification")
            return tmp
        except:
            logging.warn(f"[Component {componentId}] Error while creating the classification")
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
            combobox.config(height=min(configuration["classification"]["height"], len(combobox["values"])))
        entry.set(value="")
    addButton = tk.Button(hiddableFrame, text="Add", command=add)
    addButton.grid(row=1, column=1, sticky=[tk.W, tk.E])

    # let the user add a new classification in the configuration
    def addToConfig():
        value = entry.get()
        if (value and value not in configuration["choices"]):
            configuration["classification"]["choices"].append(value)
        add()
        entry.set(value="")
    addConfigButton = tk.Button(hiddableFrame, text="Add to configuration", command=addToConfig)
    addConfigButton.grid(row=1, column=2, sticky=[tk.W, tk.E])

    # let the user remove a classification from the configuration
    def removeFromConfig():
        selection = combobox.get()
        if (selection and selection in configuration["choices"]):
            configuration["classification"]["choices"].remove(selection)
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
def makeCommentFrame(root: tk.Frame, valueHolder: dict) -> tk.Frame:
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
# TODO: add a text inside showing if it's a description or comment component
def makeDescriptionFrame(root: tk.Frame, valueHolder: dict, componentId: uuid) -> tk.Frame:
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

    def getDescription():
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
        truc = Description(text, altrep, language)
        return truc
    valueHolder["getValue"] = getDescription

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
        values=[value[1] for value in configuration["language"]["choices"]],
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
        try:
            language = None
            altrepValue = None
            if (state.get()):
                for [key, value] in configuration["language"]["choices"]:
                    if (value == languageCombobox.get()):
                        language = key
                        break
            tmp = Location(entry.get(), altrepValue, language)
            # logging.debug(f"{entry.get()} location successfully created")
            return tmp
        except:
            logging.warn(f"[Component {componentId}] Location creation failed ({entry.get()})")
            return None
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

def makePriorityFrame(root: tk.Frame, valueHolder: dict, componentId: uuid) -> tk.Frame:
    frame = tk.Frame(root)
    frame.rowconfigure(0, weight=0)
    frame.columnconfigure(0, weight=0)
    frame.columnconfigure(1, weight=0)

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
    frame = ttk.LabelFrame(root, text="Required resources")
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=0)

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
        values=[value[1] for value in configuration["language"]["choices"]],
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
            for [key, value] in configuration["language"]["choices"]:
                if (value == languageCombobox.get()):
                    language = key
                    break
        try:
            tmp = Summary(title.get(), altrepValue, language)
            # logging.debug(f"[Component {componentId}] Summary successfully created")
            return tmp
        except:
            logging.error(f"[Component {componentId}] Unable to create summary ({title.get()})")
            return None
    valueHolder["getValue"] = getSummary
    # to be able to display the title in real time
    valueHolder["titleEntry"] = summaryEntry

    return frame
