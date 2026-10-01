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

    summaryFrame, summaryDict = makeSummaryFrame(eventFrame, configuration)
    summaryFrame.pack()

    dtStartFrame, dtStartDict = makeDtFrame(eventFrame, configuration, "start")
    dtStartFrame.pack()

    dtendFrame, dtEndDict = makeDtFrame(eventFrame, configuration, "end")
    dtendFrame.pack()

    attachmentFrame, attachmentDict = makeAttachmentFrame(eventFrame, configuration)
    attachmentFrame.pack()

    categoriesFrame, categoriesDict = makeCategoriesFrame(eventFrame, configuration)
    categoriesFrame.pack()

    classificationFrame, classificationCombobox = makeClassificationFrame(eventFrame, configuration)
    classificationFrame.pack()

    commentFrame, commentDict = makeCommentFrame(eventFrame, configuration)
    commentFrame.pack()

    descriptionFrame, descriptionDict = makeDescriptionFrame(eventFrame, configuration)
    descriptionFrame.pack()

    geoFrame, geoDict = makeGeoFrame(eventFrame, configuration)
    geoFrame.pack()

    locationFrame, locationDict = makeLocationFrame(eventFrame, configuration)
    locationFrame.pack()
   
    priorityFrame, priorityVar = makePriorityFrame(eventFrame)
    priorityFrame.pack()

    resourceFrame, resourceDict = makeResourceFrame(eventFrame, configuration)
    resourceFrame.pack()

    statusFrame, statusCombobox = makeStatusFrame(eventFrame, configuration, "event")
    statusFrame.pack()

    def createEvent():
        tmstmp = datetime.now()

        summary = None
        if (summaryDict["value"].get() != ""):
            summary = Summary(summaryDict["value"].get(), summaryDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], summaryDict["language"].get()))
        else:
            raise Exception(f"An event has to show a title, please put a title")

        dtstart = None
        if (dtStartDict["date"].get()):
            truc = dtStartDict["date"].get().split('/')
            dtstart = datetime.strptime(f"{truc[0]}-{truc[1]}-{truc[2]}", "%Y-%m-%d")
            if (dtStartDict["time"]):
                dtstart = dtstart.replace(
                    hour=int(dtStartDict["hour"].get()),
                    minute=int(dtStartDict["minute"].get()),
                    second=int(dtStartDict["second"].get())
                )

        dtend = None
        if (dtEndDict["date"].selection_get()):
            truc = dtEndDict["date"].get().split('/')
            dtend = datetime.strptime(f"{truc[0]}-{truc[1]}-{truc[2]}", "%Y-%m-%d")
            if (dtEndDict["time"]):
                dtend = dtend.replace(
                    hour=int(dtEndDict["hour"].get()),
                    minute=int(dtEndDict["minute"].get()),
                    second=int(dtEndDict["second"].get())
                )

        categories = None
        if (len(categoriesDict["listbox"].curselection()) != 0):
            categories = Categories([categoriesDict["listbox"].get(index) for index in categoriesDict["listbox"].curselection()])

        attachment = None
        if (attachmentDict["value"].get() and attachmentDict["value"] != ""):
            attachment = Attachement(attachmentDict["value"].get(), typename=attachmentDict["fmttype"]["type"].get(), subtypename=attachmentDict["fmttype"]["subtype"].get())

        classification = None
        if (classificationCombobox.get() != ""):
            classification = Classification(classificationCombobox.get())

        comment = None
        if (commentDict["value"].get("1.0", "end-1c") != ""):
            comment = Comment(commentDict["value"].get("1.0", "end-1c"), commentDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], commentDict["language"].get()))

        description = None
        if (descriptionDict["value"].get("1.0", "end-1c") != ""):
            description = Description(descriptionDict["value"].get("1.0", "end-1c"), descriptionDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], descriptionDict["language"].get()))
        
        geo = None
        try:
            geo = Geo(float(geoDict["lat"].get()), (geoDict["long"].get()))
        except Exception as _:
            pass

        location = None
        if (locationDict["value"].get("1.0", "end-1c") != ""):
            location = Location(locationDict["value"].get("1.0", "end-1c"), locationDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], locationDict["language"].get()))

        priority = None
        if (priorityVar.get() != ""):
            priority = Priority(int(priorityVar.get()))

        # TODO: check why stringify doesn't work
        resource = None
        if (resourceDict["value"].get("1.0", "end-1c") != ""):
            resource = Resources(resourceDict["value"].get("1.0", "end-1c"), resourceDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], resourceDict["language"].get()))

        status = None
        if (statusCombobox.get() != ""):
            status = Status(statusCombobox.get())

        event = Vevent(
            tmstmp,
            dtstart=dtstart,
            end=dtend,
            classification=classification,
            description=description,
            attach=attachment,
            categories=categories,
            comment=comment,
            geo=geo,
            location=location,
            priority=priority,
            # resources=[resource],
            status=status,
            title=summary
        )
        print(event)
        eventObject["value"] = event


    addButton = tk.Button(eventFrame, text="Add event", command=createEvent)
    addButton.pack()

    return eventFrame, eventObject