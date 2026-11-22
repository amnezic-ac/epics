from tkinter import ttk
import tkinter as tk

from src.backend.parameters import *
from src.utils import configuration, logging

# TODO: implement add/remove calendar address (delegated from and to), dir
# TODO: understand ATTACH property and its parameters

def makeAlternativeRepresentationFrame(root: tk.Frame, valueHolder: dict) -> tk.Frame:
    frame = ttk.Labelframe(root, text="Alternative representation")

    altrepText = tk.Text(
        frame,
        width = configuration["altrep"]["width"],
        height = configuration["altrep"]["height"]
    )
    altrepText.grid(row=0, column=0)
    
    scrollbar = ttk.Scrollbar(
        frame,
        orient="vertical",
        command=altrepText.yview,
    )
    scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    altrepText["yscrollcommand"] = scrollbar.set

    def getAltrep():
        value = txt.get('1.0', 'end')
        if (not text or not text.strip()):
            return None
        return value.strip()
    valueHolder["getValue"] = getAltrep

    return frame

# NOTE: This parameter can be specified on properties with a CAL-ADDRESS value type
def makeCommonNameFrame(root: tk.Frame, valueHolder: dict) -> tk.Frame:
    frame = ttk.Labelframe(root, text="Common name")

    entry = ttk.Entry(
        frame,
        width=configuration["common-name"]["width"]
    )
    entry.grid()

    def getCN():
        value = entry.get()
        if (not value.strip()):
            return None
        return Cn(value)
    valueHolder["getValue"] = getCN

    return frame

def makeCutypeFrame(root: tk.Frame, valueHolder: dict) -> tk.Frame:
    frame = ttk.Labelframe(root, text="Who is the calendar user ?")

    cutype = tk.StringVar()
    combobox = ttk.Combobox(
        frame,
        textvariable=cutype,
        values=configuration["cutype"]["choices"],
        state="readonly",
        height=min(configuration["cutype"]["height"], len(configuration["cutype"]["choices"]))
    )
    combobox.bind('<<ComboboxSelected>>', lambda e: e.widget.selection_clear())
    combobox.grid(row=0, column=0, sticky=tk.N)

    entry = ttk.Entry(
        frame,
        width=configuration["cutype"]["width"],
    )
    entry.grid(row=0, column=1)

    def add():
        value = entry.get()
        if (value):
            combobox["values"].append(value.strip().upper())
        else:
            logging.warn(f"User tried to add an empty calendar user type")
    addButton = ttk.Button(frame, text="Add entry", command=add)
    addButton.grid(row=1, column=1, sticky=(tk.W, tk.E))

    def remove():
        tmp = list(combobox["values"])
        tmp.remove(combobox.get())
        combobox["values"] = tmp
        combobox.set(combobox["values"][0])
    removeButton = ttk.Button(frame, text="Remove selection", command=remove)
    removeButton.grid(row=1, column=0,  sticky=(tk.W, tk.E))

    def getCutype():
        value = cutype.get()
        if (not value or not value.strip()):
            return None
        return value.strip()
    valueHolder["getValue"] = getCutype

    return frame

def makeFreeBusyTimeFrame(root: tk.Frame, valueHolder: dict) -> tk.Frame:
    frame = ttk.LabelFrame(root, text="Free or busy ?")

    combobox = ttk.Combobox(
        frame,
        values=configuration["fbttype"]["choices"],
        state="readonly",
        height=min(configuration["fbttype"]["height"], len(configuration["fbttype"]["choices"]))
    )
    combobox.grid(row=0, column=0)

    entry = ttk.Entry(
        frame,
        width = configuration["fbttype"]["width"]
    )
    entry.grid(row=0, column=1)

    def add():
        value = entry.get()
        if (not value or not value.strip()):
            logging.warn(f"User tried to add an empty freebusy time type")
        else:
            tmp = list(combobox["values"])
            tmp.append(value.strip().upper())
            combobox["values"] = tmp
            combobox.set(combobox["values"][-1])
            entry.delete(0, "end")
    addButton = ttk.Button(frame, text="Add entry", command=add)
    addButton.grid(row=1, column=1, sticky=(tk.W, tk.E))

    def remove():
        value = combobox.get()
        if (not value):
            logging.warn(f"User tried to remove freebusy time selection but no selection yet")
            return None
        tmp = list(combobox["values"])
        tmp.remove(value)
        combobox["values"] = tmp
        combobox.set(combobox["values"][0])
    removeButton = ttk.Button(frame, text="Remove selection", command=remove)
    removeButton.grid(row=1, column=0, sticky=(tk.W, tk.E))

    def getFBT():
        value = combobox.get()
        if (not value or not value.strip()):
            return None
    valueHolder["getValue"] = getFBT

    return frame

def makeLanguageFrame(root: tk.Frame, valueHolder: dict) -> tk.Frame:
    frame = ttk.LabelFrame(root, text="Language")

    combobox = ttk.Combobox(
        frame,
        state="readonly",
        values=[elt[1] for elt in configuration["language"]["choices"]],
        height=min(configuration["language"]["height"], len(configuration["language"]["choices"]))
    )
    combobox.grid()

    def getLanguageKey():
        value = combobox.get()
        if (not value or not value.strip()):
            return None
        value = value.strip()
        for pair in configuration["language"]["choices"]:
            if (pair[1] == value):
                return pair[0]
        logging.debug(f"User choose a language value from GUI but value ({value}) does not have key")
        return None
    valueHolder["getValue"] = getLanguageKey

    return frame

def makePartstatFrame(root: tk.Frame, componentType: str, valueHolder: dict) -> tk.Frame :
    if (not componentType in ["event", "todo", "journal"]):
        raise Exception(f"{componentType} is invalid component type, should be \"event\", \"todo\" or \"journal\"")

    frame = ttk.LabelFrame(root, text="Participation status")

    combobox = ttk.Combobox(
        frame,
        state="readonly",
        values=configuration["partstat"][f"{componentType}"],
        height=min(configuration["partstat"]["height"], len(configuration["partstat"][f"{componentType}"]))
    )
    combobox.grid()

    def getValue():
        value = combobox.get()
        if (not value or not value.strip()):
            return None
        return value.strip()
    valueHolder["getValue"] = getValue

    return frame

def makeRelationshipFrame(root: tk.Frame, valueHolder: dict) -> tk.Frame :
    """
        This parameter can be specified on a property that
        references another related calendar.  The parameter specifies the
        hierarchical relationship type of the calendar component
        referenced by the property.
    """
    frame = ttk.LabelFrame(root, text="Relationship")

    combobox = ttk.Combobox(
        frame,
        state="readonly",
        values=configuration["relationship"]["choices"],
        height=min(configuration["relationship"]["height"], len(configuration["relationship"]["choices"]))
    )
    combobox.grid(column=0, row=0)

    entry = ttk.Entry(frame, width=configuration["relationship"]["width"])
    entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

    def add():
        value = entry.get()
        if (value and value.strip()):
            value = value.strip()
            tmp = list(combobox["values"])
            tmp.append(value)
            combobox["values"] = tmp
            combobox.set(value)
    addButton = ttk.Button(frame, text="Add entry", command=add)
    addButton.grid(row=1, column=1, sticky=(tk.W, tk.E))

    def remove():
        value = combobox.get()
        if (value and value.strip()):
            value = value.strip()
            tmp = list(combobox["values"])
            tmp.remove(value)
            combobox["values"] = tmp
            combobox.set(combobox["values"][0])
    removeButton = ttk.Button(frame, text="Remove selection", command=remove)
    removeButton.grid(row=1, column=0, sticky=(tk.W, tk.E))

    def getRelationship():
        value = combobox.get()
        if (not value or not value.strip()):
            return None
        return value.strip()
    valueHolder["getValue"] = getRelationship

    return frame

def makeRoleFrame(masterFrame):
    roleFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(roleFrame)
    userFrame = tk.Frame(hiddableFrame)
    roleInput = ttk.Combobox(
        userFrame,
        values=configuration["role"]["choices"],
        state="readonly"
    )
    roleInput.pack()
    userEntry = tk.Entry(userFrame)
    userEntry.pack()
    userFrame.pack(side="left")

    buttonState = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (buttonState.get()):
            hiddableFrame.pack(side="right")
            checkbutton.config(text="Role : ")
        else:
            hiddableFrame.pack_forget()
            checkbutton.config(text="Role ? ")
    checkbutton = tk.Checkbutton(roleFrame, text="Role ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    checkbutton.pack(side="left")

    # maybe useful for later development
    # def add():
    #     value = userEntry.get()
    #     values = list(roleInput["values"])
    #     if value and value not in values:
    #         values.append(value)
    #         roleInput["values"] = values
    #         roleInput.set(roleInput["values"][-1])

    # def addToConfiguration():
    #     value = userEntry.get()
    #     if value and value not in configuration["role"]["choices"]:
    #         add()
    #         configuration["role"]["choices"].append(value)

    # def remove():
    #     value = roleInput.get()
    #     values = list(roleInput["values"])
    #     if value in values:
    #         values.remove(value)
    #         roleInput["values"] = values
    #         if (len(values) != 0):
    #             roleInput.set(roleInput["values"][0])
    #         else:
    #             roleInput.set("")

    # def removeFromConfiguration():
    #     value = roleInput.get()
    #     if value in configuration["role"]["choices"]:
    #         remove()
    #         configuration["role"]["choices"].remove(value)

    # buttonsFrame = tk.Frame(roleFrame)
    # tk.Button(buttonsFrame, text="Add", command=add).pack()
    # tk.Button(buttonsFrame, text="Add to configuration", command=addToConfiguration).pack()
    # tk.Button(buttonsFrame, text="Remove", command=remove).pack()
    # tk.Button(buttonsFrame, text="Remove from configuration", command=removeFromConfiguration).pack()
    # buttonsFrame.pack(side="right")

    return roleFrame, roleInput

def makeRsvpFrame(root: tk.Frame, valueHolder: dict) -> tk.Frame :
    frame = tk.LabelFrame(root, text="RSVP")

    combobox = ttk.Combobox(
        frame,
        state="readonly",
        values=configuration["rsvp"]["choices"],
        height=min(configuration["rsvp"]["height"], len(configuration["rsvp"]["choices"]))
    )
    combobox.grid()

    # NOTE: maybe useful for later but for now, user won't be able to add RSVP choices
    # entry = ttk.Entry(frame, width=configuration["rsvp"]["width"])
    # entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
    # def add():
    #     value = entry.get()
    #     if (value and value.strip()):
    #         value = value.strip()
    #         tmp = list(combobox["values"])
    #         tmp.append(value)
    #         combobox["values"] = tmp
    #         combobox.set(value)
    # addButton = ttk.Button(frame, text="Add entry", command=add)
    # addButton.grid(row=1, column=1, sticky=(tk.W, tk.E))

    # def remove():
    #     value = combobox.get()
    #     if (value and value.strip()):
    #         value = value.strip()
    #         tmp = list(combobox["values"])
    #         tmp.remove(value)
    #         combobox["values"] = tmp
    #         combobox.set(combobox["values"][0])
    # removeButton = ttk.Button(frame, text="Remove selection", command=remove)
    # removeButton.grid(row=1, column=0, sticky=(tk.W, tk.E))

    def getRSVP():
        value = combobox.get()
        if (not value or not value.strip()):
            return None
        return value.strip()
    valueHolder["getValue"] = getRSVP

    return frame    

def makeSentByFrame(masterFrame):
    sentByFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(sentByFrame)
    value = tk.StringVar(value="")
    sentByInput = tk.Entry(hiddableFrame, textvariable=value)
    sentByInput.pack()
    
    buttonState = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (buttonState.get()):
            hiddableFrame.pack(side="right")
            checkbutton.config(text="Sent by : ")
        else:
            hiddableFrame.pack_forget()
            checkbutton.config(text="Sent by ? ")
    checkbutton = tk.Checkbutton(sentByFrame, text="Sent by ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    checkbutton.pack(side="left")

    sentbyDict = {
        "state": buttonState,
        "value": value
    }

    return sentByFrame, sentbyDict

# def makeMemberFrame(masterFrame):
#     memberFrame = tk.Frame(masterFrame)
# 
#     hiddableFrame = tk.Frame(memberFrame)
#     inputFrame = tk.Frame(hiddableFrame)
#     value = tk.StringVar(value="")
#     memberInput = ttk.Combobox(
#         inputFrame,
#         values=configuration["member"]["choices"],
#         state="readonly",
#         textvariable=value
#     )
#     memberInput.pack()
#     userEntry = tk.Entry(inputFrame)
#     userEntry.pack()
#     inputFrame.pack(side="left")
# 
#     def add():
#         value = userEntry.get()
#         values = list(memberInput["values"])
#         if value and value not in values:
#             values.append(value)
#             memberInput["values"] = values
#             memberInput.set(memberInput["values"][-1])
#             userEntry.delete(0, tk.END)
# 
#     def addToConfiguration():
#         value = userEntry.get()
#         if value and value not in configuration["member"]["choices"]:
#             add()
#             configuration["member"]["choices"].append(value)
# 
#     def remove():
#         value = memberInput.get()
#         values = list(memberInput["values"])
#         if value in values:
#             values.remove(value)
#             memberInput["values"] = values
#             if (len(memberInput["values"]) > 0):
#                 memberInput.set(memberInput["values"][0])
#             else:
#                 memberInput.set("")
# 
#     def removeFromConfiguration():
#         value = memberInput.get()
#         if value in configuration["member"]["choices"]:
#             remove()
#             configuration["member"]["choices"].remove(value)
# 
#     buttonsFrame = tk.Frame(memberFrame)
#     tk.Button(buttonsFrame, text="Add", command=add).pack()
#     tk.Button(buttonsFrame, text="Add to configuration", command=addToConfiguration).pack()
#     tk.Button(buttonsFrame, text="Remove", command=remove).pack()
#     tk.Button(buttonsFrame, text="Remove from configuration", command=removeFromConfiguration).pack()
#     buttonsFrame.pack(side="right")
# 
#     buttonState = tk.BooleanVar(value=False)
#     def toggleHiddableFrame():
#         if (buttonState.get()):
#             hiddableFrame.pack(side="right")
#             checkbutton.config(text="Member role : ")
#         else:
#             hiddableFrame.pack_forget()
#             checkbutton.config(text="Member role ? ")
#     checkbutton = tk.Checkbutton(memberFrame, text="Member role ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleHiddableFrame)
#     checkbutton.pack(side="left")
# 
#     memberDict = {
#         "state": buttonState,
#         "value": value
#     }
# 
#     return memberFrame, memberDict
