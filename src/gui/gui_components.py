from tkinter import ttk
import tkinter as tk
from datetime import datetime, timedelta

from src.backend.components.vevent import Vevent
from src.backend.properties import *
from src.gui.gui_properties import *

# NOTE: work on period frame handler --> should do a choice between a duration and a dtend (also useful for dtstart)

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

    classificationFrame, classificationDict = makeClassificationFrame(eventFrame, configuration)
    classificationFrame.pack()

    commentFrame, commentDict = makeCommentFrame(eventFrame, configuration)
    commentFrame.pack()

    descriptionFrame, descriptionDict = makeDescriptionFrame(eventFrame, configuration)
    descriptionFrame.pack()

    geoFrame, geoDict = makeGeoFrame(eventFrame, configuration)
    geoFrame.pack()

    locationFrame, locationDict = makeLocationFrame(eventFrame, configuration)
    locationFrame.pack()
   
    priorityFrame, priorityDict = makePriorityFrame(eventFrame)
    priorityFrame.pack()

    resourceFrame, resourceDict = makeResourceFrame(eventFrame, configuration)
    resourceFrame.pack()

    statusFrame, statusDict = makeStatusFrame(eventFrame, configuration, "event")
    statusFrame.pack()

    durationFrame, durationDict = makeDurationFrame(eventFrame, configuration)
    durationFrame.pack()

    def createEvent():
        tmstmp = datetime.now()

        summary = None
        if (summaryDict["value"].get() != ""):
            summary = Summary(summaryDict["value"].get(), summaryDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], summaryDict["language"].get()))
        else:
            raise Exception(f"An event has to show a title, please put a title")

        dtstart = None
        if (dtStartDict["date-status"].get()):
            truc = dtStartDict["date"].get().split('/')
            dtstart = datetime.strptime(f"{truc[0]}-{truc[1]}-{truc[2]}", "%Y-%m-%d")
            if (dtStartDict["time-status"].get()):
                dtstart = dtstart.replace(
                    hour=int(dtStartDict["hour"].get()),
                    minute=int(dtStartDict["minute"].get()),
                    second=int(dtStartDict["second"].get())
                )

        dtend = None
        if (dtEndDict["date-status"].get()):
            truc = dtEndDict["date"].get().split('/')
            dtend = datetime.strptime(f"{truc[0]}-{truc[1]}-{truc[2]}", "%Y-%m-%d")
            if (dtEndDict["time-status"].get()):
                dtend = dtend.replace(
                    hour=int(dtEndDict["hour"].get()),
                    minute=int(dtEndDict["minute"].get()),
                    second=int(dtEndDict["second"].get())
                )

        categories = None
        if (categoriesDict["state"].get() and len(categoriesDict["listbox"].curselection()) > 0):
            categories = Categories([categoriesDict["listbox"].get(index) for index in categoriesDict["listbox"].curselection()])

        attachment = None
        if (attachmentDict["state"].get()):
            attachment = Attachement(attachmentDict["value"].get(), typename=attachmentDict["fmttype"]["type"].get(), subtypename=attachmentDict["fmttype"]["subtype"].get())

        classification = None
        if (classificationDict["state"].get()):
            classification = Classification(classificationDict["value"].get())

        comment = None
        if (commentDict["state"].get()):
            comment = Comment(commentDict["value"].get("1.0", "end-1c"), commentDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], commentDict["language"].get()))

        description = None
        if (descriptionDict["state"].get()):
            description = Description(descriptionDict["value"].get("1.0", "end-1c"), descriptionDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], descriptionDict["language"].get()))
        
        geo = None
        if (geoDict["state"].get()):
            geo = Geo(float(geoDict["lat"].get()), (geoDict["long"].get()))

        location = None
        if (locationDict["state"].get()):
            location = Location(locationDict["value"].get(), locationDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], locationDict["language"].get()))

        priority = None
        if (priorityDict["state"].get()):
            priority = Priority(int(priorityDict["value"].get()))

        # TODO: check why stringify doesn't work
        resource = None
        if (resourceDict["state"].get()):
            resource = Resources(resourceDict["value"].get("1.0", "end-1c"), resourceDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], resourceDict["language"].get()))

        status = None
        if (statusDict["state"].get()):
            status = Status(statusDict["value"].get())

        duration = None
        if (durationDict["value"].get()):
            duration = Duration(
                int(durationDict["week"].get()),
                int(durationDict["day"].get()),
                int(durationDict["hour"].get()),
                int(durationDict["minute"].get()),
                int(durationDict["second"].get())
            )

        end = None
        if (dtend and duration):
            raise Exception(f"Can't have an end date and a duration")
        elif (not dtend and not duration):
            raise Exception(f"An event has to got an end")
        else:
            if (not dtend):
                end = duration
            else:
                end = dtend

        event = Vevent(
            tmstmp,
            dtstart=dtstart,
            end=end,
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
            title=summary,
        )
        print(event)
        eventObject["value"] = event


    addButton = tk.Button(eventFrame, text="Add event", command=createEvent)
    addButton.pack()

    return eventFrame, eventObject