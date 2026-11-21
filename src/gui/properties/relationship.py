from src.gui.imports import *
from src.backend.properties.relationship import Atttendee, Organizer, Url

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