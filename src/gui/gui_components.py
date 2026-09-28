from tkinter import ttk
import tkinter as tk
from datetime import datetime, timedelta

from src.backend.components.vevent import Vevent
from src.backend.properties import *
from src.gui.gui_properties import *

def findLangIdFromLangValue(configuration, value_):
    for language in configuration:
        for key, value in language.items():
            if (value == value_):
                return key
    return None

def makeEventFrame(masterFrame, configuration):
    eventFrame = tk.Frame(masterFrame)
    eventObject = {"value": None}

    attachmentFrame, attachmentDict = makeAttachmentFrame(eventFrame, configuration)
    attachmentFrame.pack()

    categoriesFrame, categoriesDict = makeCategoriesFrame(eventFrame, configuration)
    categoriesFrame.pack()

    classificationFrame, classificationCombobox = makeClassificationFrame(eventFrame, configuration)
    classificationFrame.pack()

    commentFrame, commentDict = makeCommentFrame(eventFrame, configuration)
    commentFrame.pack()

    def createEvent():
        tmstmp = datetime.now()

        categories = Categories([categoriesDict["listbox"].get(index) for index in categoriesDict["listbox"].curselection()])
        attachment = Attachement(attachmentDict["value"].get(), typename=attachmentDict["fmttype"]["type"].get(), subtypename=attachmentDict["fmttype"]["subtype"].get())
        classification = Classification(classificationCombobox.get())
        comment = Comment(commentDict["value"].get("1.0", "end-1c"), commentDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], commentDict["language"].get()))
        print(comment)

        event = Vevent(tmstmp, tmstmp, tmstmp + timedelta(hours=2), categories=categories)
        eventObject["value"] = event


    addButton = tk.Button(eventFrame, text="Add event", command=createEvent)
    addButton.pack()

    return eventFrame, eventObject