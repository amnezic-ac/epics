from tkinter import ttk
import tkinter as tk
from src.gui.gui_parameters import *

# NOTE: put the user input part in a hiddable frame iff the frame is optional for all the types of event it can appears

def makeAttachmentFrame(masterFrame, configuration):
    attachmentFrame = tk.Frame(masterFrame)
    attachmentParameters = {}

    fmttypeFrame, fmttypeInput = makeFmtTypeFrame(attachmentFrame)
    fmttypeFrame.pack()

    return attachmentFrame, attachmentParameters

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
    def toggleCategoriesEntry():
        if (buttonState.get()):
            hiddableFrame.pack(side="right")
        else:
            hiddableFrame.pack_forget()
    checkbutton = tk.Checkbutton(categoriesFrame, text="Categories ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleCategoriesEntry)
    checkbutton.pack(side="left")

    categoriesDict = {
        "listbox": listbox,
        "language": languageInput
    }

    return categoriesFrame, categoriesDict