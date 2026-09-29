from tkinter import ttk
import tkinter as tk
from src.gui.gui_parameters import *

# NOTE: put the user input part in a hiddable frame iff the frame is optional for all the types of event it can appears
# TODO: implement geo frame

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
            hiddableFrame.pack(side="right")
            checkbutton.config(text="Attachment : ")
        else:
            hiddableFrame.pack_forget()
            checkbutton.config(text="Attachment ? ")
    checkbutton = tk.Checkbutton(attachmentFrame, text="Attachment ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    checkbutton.pack(side="left")

    attachmentDict = {
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

def makeClassificationFrame(masterFrame, configuration):
    classificationFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(classificationFrame)
    combobox = ttk.Combobox(
        hiddableFrame,
        values=configuration["classification"]["choices"],
        state="readonly"
    )
    combobox.pack()

    buttonState = tk.BooleanVar(value=False)
    def toggleCategoriesEntry():
        if (buttonState.get()):
            checkbutton.config(text="Classification : ")
            hiddableFrame.pack(side="right")
        else:
            checkbutton.config(text="Classification ? ")
            hiddableFrame.pack_forget()
    checkbutton = tk.Checkbutton(classificationFrame, text="Classification ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleCategoriesEntry)
    checkbutton.pack(side="left")

    return classificationFrame, combobox

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
    def toggleCategoriesEntry():
        if (buttonState.get()):
            checkbutton.config(text="Comment : ")
            hiddableFrame.pack(side="right")
        else:
            checkbutton.config(text="Comment ? ")
            hiddableFrame.pack_forget()
    checkbutton = tk.Checkbutton(commentFrame, text="Comment ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleCategoriesEntry)
    checkbutton.pack(side="left")

    commentDict = {
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
    def toggleCategoriesEntry():
        if (buttonState.get()):
            checkbutton.config(text="Description : ")
            hiddableFrame.pack(side="right")
        else:
            checkbutton.config(text="Description ? ")
            hiddableFrame.pack_forget()
    checkbutton = tk.Checkbutton(descriptionFrame, text="Description ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleCategoriesEntry)
    checkbutton.pack(side="left")

    descriptionDict = {
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
    latSpinbox.pack()
    tk.Label(hiddableFrame, text=" ; ").pack(side="right")
    longVar = tk.StringVar(value="")
    longSpinbox = ttk.Spinbox(hiddableFrame, from_=-180.000000, to=180.000000, wrap=True, increment=0.000001, textvariable=longVar)
    longSpinbox.pack(side="right")

    buttonState = tk.BooleanVar(value=False)
    def toggleCategoriesEntry():
        if (buttonState.get()):
            checkbutton.config(text="Geographic position : ")
            hiddableFrame.pack(side="right")
        else:
            checkbutton.config(text="Geographic position ? ")
            hiddableFrame.pack_forget()
    checkbutton = tk.Checkbutton(geoFrame, text="Geographic position ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleCategoriesEntry)
    checkbutton.pack(side="left")

    geoDict = {
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
    def toggleCategoriesEntry():
        if (buttonState.get()):
            checkbutton.config(text="Location : ")
            hiddableFrame.pack(side="right")
        else:
            checkbutton.config(text="Location ? ")
            hiddableFrame.pack_forget()
    checkbutton = tk.Checkbutton(locationFrame, text="Location ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleCategoriesEntry)
    checkbutton.pack(side="left")

    locationDict = {
        "value": locationText,
        "altrep": altrepInput,
        "language": languageInput
    }

    return locationFrame, locationDict