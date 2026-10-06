from tkinter import ttk
import tkinter as tk
from datetime import datetime, timedelta

from src.backend.components.vevent import Vevent
from src.backend.properties import *
from src.gui.gui_properties import *
from utils import configuration, logging

# TODO
"""
- url
- organizer/attendee
- contact
- attach
- related
- resources
- seq
- recurid
- rrule
- exdate
- rstatus: related to how the software deal with the component (maybe for later)
- rdate
"""

def findLangIdFromLangValue(configuration, value_):
    for language in configuration:
        for key, value in language.items():
            if (value == value_):
                return key
    return None

def makeEventFrame(masterFrame):
    logging.debug("New frame event opened")

    title = tk.StringVar(value=None)
    main = tk.Toplevel(masterFrame)
    def updateEventTitle(*args):
        main.title(title.get())
    title.trace("w", updateEventTitle)

    for i in range(8):
        main.rowconfigure(i, weight = 1)
    for i in range(2):
        main.columnconfigure(i, weight = 1)

    summaryFrame, summaryDict = makeSummaryFrame(main, title)
    summaryFrame.grid(column=0, row=0, sticky=tk.W)

    statusFrame, statusValue = makeStatusFrame(main, "event")
    statusFrame.grid(column=1, row=0, sticky=tk.E)

    dtStartFrame, dtStartDict = makeDtFrame(main, "start")
    dtStartFrame.grid(column=0, row=1, sticky=tk.W)

    endFrame = tk.Frame(main)
    endFrame.rowconfigure(0)
    endFrame.rowconfigure(1)
    endFrame.columnconfigure(0)
    endFrame.columnconfigure(1)
    endChoice = tk.StringVar(value="")
    dtendFrame, dtendDict = makeDtFrame(endFrame, "end")
    durationFrame, durationDict = makeDurationFrame(endFrame)
    durationUsed = tk.BooleanVar(value=False)
    def toggleDtFrame():
        durationUsed.set(False)
        dtendFrame.grid(row=0, column=1)
        if (durationFrame):
            durationFrame.grid_forget()
    dtButton = ttk.Radiobutton(endFrame, text="Date", value="date", variable=endChoice, command=toggleDtFrame)
    dtButton.grid(row=0, column=0, sticky=tk.W)
    def toggleDurationFrame():
        durationUsed.set(True)
        durationFrame.grid(row=1, column=1)
        if (dtendFrame):
            dtendFrame.grid_forget()
    durationButton = ttk.Radiobutton(endFrame, text="Duration", value="duration", variable=endChoice, command=toggleDurationFrame)
    durationButton.grid(row=1, column=0, sticky=tk.W)
    endFrame.grid(row=1, column=1, sticky=tk.E)

    locationFrame, locationDict = makeLocationFrame(main)
    locationFrame.grid(column=0, row=2, sticky=tk.W)

    organizerFrame, organizerListbox = makeAttendeeFrame(main, "event", "Organizer: ")
    organizerFrame.grid(row=3, column=0, sticky=tk.W)

    attendeesFrame, attendeesListbox = makeAttendeeFrame(main, "event", "Attendees: ")
    attendeesFrame.grid(row=4, column=0, sticky=tk.W)

    attachmentFrame, attachmentDict = makeAttachmentFrame(main)
    attachmentFrame.grid(row=5, column=0, sticky=tk.W)

    categoriesFrame, categoriesDict = makeCategoriesFrame(main)
    categoriesFrame.grid(row=5, column=1, sticky=tk.E)

    descriptionFrame, descriptionDict = makeDescriptionFrame(main)
    descriptionFrame.grid(row=6, column=0, columnspan=2, sticky=tk.W)

    labelPlus = tk.Label(main, text="Show more ?")
    labelPlus.grid(row=7, column=0, sticky=tk.EW)

    submitButton = tk.Button(main, text="Confirm")
    submitButton.grid(row=7, column=1)

    informationsFrame = tk.Frame(main)
    for i in range(9):
        informationsFrame.rowconfigure(i, weight=1)
    for i in range(2):
        informationsFrame.columnconfigure(i, weight=1)

    classificationFrame, classificationDict = makeClassificationFrame(informationsFrame)
    classificationFrame.grid(row=0, column=0, sticky=tk.W)

    priorityFrame, priorityDict = makePriorityFrame(informationsFrame)
    priorityFrame.grid(row=0, column=1, sticky=tk.E)

    tranparencyFrame, transpDict = makeTranspFrame(informationsFrame)
    tranparencyFrame.grid(row=1, column=0, sticky=tk.W)

    geoFrame, geoDict = makeGeoFrame(informationsFrame)
    geoFrame.grid(row=1, column=1, sticky=tk.E)

    urlFrame, urlValue = makeURLFrame(informationsFrame)
    urlFrame.grid(row=2, column=0, rowspan=2, sticky=tk.W)

    commentFrame, commentDict = makeCommentFrame(informationsFrame)
    commentFrame.grid(column=0, row=4, columnspan=2, sticky=tk.EW)

    labelMinus = tk.Label(informationsFrame, text="Show less ?")
    labelMinus.grid(row=8, column=0)
    submitButton2 = tk.Button(informationsFrame, text="Confirm")
    submitButton2.grid(row=8, column=1)
    
    state = tk.BooleanVar(value=False)
    def toggleHiddableFrame(event):
        actual = not state.get()
        if (actual):
            labelPlus.grid_forget()
            informationsFrame.grid(row=7, column=0, columnspan=2, sticky=tk.EW)
        else:
            informationsFrame.grid_forget()
            labelPlus.grid(row=7, column=0, columnspan=2, sticky=tk.EW)
        state.set(actual)
    labelPlus.bind('<Double-1>', toggleHiddableFrame)
    labelMinus.bind('<Double-1>', toggleHiddableFrame)

    eventDict = {"value":None}
    def submit():
        # mandatory properties
        summary = None  # not a mandatory property in theory but got no sense withtout it
        if (not summaryDict["value"].get()):
            raise Exception(f"The event has to got a title")
        summary = Summary(summaryDict["value"].get())

        dtstart = None
        if (not dtStartDict["date"].get()):
            raise Exception(f"An event has to got a start date")
        else:
            truc = dtStartDict["date"].get().split('/')
            dtstart = datetime.strptime(f"{truc[0]}-{truc[1]}-{truc[2]}", "%Y-%m-%d")
            if (dtStartDict["time-status"].get()):
                dtstart = dtstart.replace(
                    hour=int(dtStartDict["hour"].get()),
                    minute=int(dtStartDict["minute"].get()),
                    second=int(dtStartDict["second"].get())
                )
        
        end = None
        if (durationUsed):
            end = Duration(
                int(durationDict["week"].get()),
                int(durationDict["day"].get()),
                int(durationDict["hour"].get()),
                int(durationDict["minute"].get()),
                int(durationDict["second"].get())
            )
        else:
            truc = dtEndDict["date"].get().split('/')
            end = datetime.strptime(f"{truc[0]}-{truc[1]}-{truc[2]}", "%Y-%m-%d")
            if (dtEndDict["time-status"].get()):
                dtend = dtend.replace(
                    hour=int(dtEndDict["hour"].get()),
                    minute=int(dtEndDict["minute"].get()),
                    second=int(dtEndDict["second"].get())
                )

        categories = None
        if (len(categoriesDict["listbox"].curselection()) > 0):
            categories = Categories([categoriesDict["listbox"].get(index) for index in categoriesDict["listbox"].curselection()])

        # attachment = None
        # if (attachmentDict["state"].get()):
        #     attachment = Attachement(attachmentDict["value"].get(), typename=attachmentDict["fmttype"]["type"].get(), subtypename=attachmentDict["fmttype"]["subtype"].get())

        classification = None
        if (classificationDict["value"].get()):
            classification = Classification(classificationDict["value"].get())

        comment = None
        if (commentDict["value"].get("1.0", "end-1c")):
            comment = Comment(commentDict["value"].get("1.0", "end-1c"), commentDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], commentDict["language"].get()))

        description = None
        if (descriptionDict["value"].get("1.0", "end-1c")):
            description = Description(descriptionDict["value"].get("1.0", "end-1c"), descriptionDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], descriptionDict["language"].get()))
        
        geo = None
        if (geoDict["lat"].get() and geoDict["long"].get()):
            geo = Geo(float(geoDict["lat"].get()), (geoDict["long"].get()))

        location = None
        if (locationDict["value"].get("1.0", "end-1c")):
            location = Location(locationDict["value"].get("1.0", "end-1c"), locationDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], locationDict["language"].get()))

        priority = None
        if (priorityDict["value"].get()):
            priority = Priority(int(priorityDict["value"].get()))

        # TODO: check why stringify doesn't work
        # resource = None
        # if (resourceDict["state"].get()):
        #     resource = Resources(resourceDict["value"].get("1.0", "end-1c"), resourceDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], resourceDict["language"].get()))

        status = None
        if (statusValue.get()):
            status = Status(statusValue.get())

        transp = None
        if (transpDict["value"].get()):
            transp = Transparency(transpDict["value"].get())

        url = None
        if (urlValue.get()):
            url = Url(urlValue.get())

        tmstamp = datetime.now()
        event = Vevent(
            tmstamp,
            dtstart,
            end,
            classification,
            tmstamp,
            description,
            geo,
            datetime.now(),
            location,
            None,
            priority,
            None,
            status,
            summary,
            transp,
            None,
            None,
            categories,
            comment,
            None,
            None,
            url
        )
        eventDict["value"] = event
        print(event)
        logging.debug(f"\"{title.get()}\" event has successfully been created")

    submitButton.config(
        command=submit
    )
    submitButton2.config(
        command=submit
    )

    return main, eventDict