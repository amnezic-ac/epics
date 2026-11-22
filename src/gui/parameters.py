from tkinter import ttk
import tkinter as tk

from src.backend.parameters import *
from src.utils import configuration, logging

"""
TODO
- understand how to use cal-addresses
- fix the timezone management:
    * check for the good timezone for Paris
    * add the offset to datetime of the components
    * let the user change on the GUI the offset
        * think about the situation where the user modify the offset after having confirmed some components
- implement the following parameters (by decreasing order of importance):
    * group or list member ship
    * delegators
    * delegatees
    * directory entry reference
    * format type
    * alarm trigger relationship
    * Recurrence Identifier Range (for later because I don't understand anything)
"""

# TODO: implement add/remove calendar address (delegated from and to), dir, sent-by
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

def makeRoleFrame(root: tk.Frame, valueHolder: dict) -> tk.Frame:
    frame = ttk.LabelFrame(root, text="Role")

    combobox = ttk.Combobox(
        frame,
        state="readonly",
        values=configuration["role"]["choices"],
        height=min(configuration["role"]["height"], len(configuration["role"]["choices"]))
    )
    combobox.grid(column=0, row=0)

    entry = ttk.Entry(frame, width=configuration["role"]["width"])
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

    def getRole():
        value = combobox.get()
        if (not value or not value.strip()):
            return None
        return value.strip()
    valueHolder["getValue"] = getRole

    return frame

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
