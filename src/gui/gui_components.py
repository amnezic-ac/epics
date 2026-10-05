from tkinter import ttk
import tkinter as tk
from datetime import datetime, timedelta

from src.backend.components.vevent import Vevent
from src.backend.properties import *
from src.gui.gui_properties import *
from utils import configuration, logging

# NOTE: work on period frame handler --> should do a choice between a duration and a dtend (also useful for dtstart)

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
    endChoice = tk.StringVar(value="")
    dtButton = ttk.Radiobutton(endFrame, text="Date", value="date", variable=endChoice)
    dtButton.pack()
    durationButton = ttk.Radiobutton(endFrame, text="Duration", value="duration", variable=endChoice)
    durationButton.pack()
    # dtEndFrame, dtEndDict = makeDtFrame(main, "end")
    # dtEndFrame.grid(column=1, row=1)
    endFrame.grid(row=1, column=1, sticky=tk.E)

    locationFrame, locationDict = makeLocationFrame(main)
    locationFrame.grid(column=0, row=2, sticky=tk.W)

    organizerFrame = makeAttendeeFrame(main, "event", "Organizer: ")
    organizerFrame.grid(row=3, column=0, sticky=tk.W)

    attendeesFrame = makeAttendeeFrame(main, "event", "Attendees: ")
    attendeesFrame.grid(row=4, column=0, sticky=tk.W)

    attachmentFrame, attachmentDict = makeAttachmentFrame(main)
    attachmentFrame.grid(row=5, column=0, sticky=tk.W)

    categoriesFrame, categoriesDict = makeCategoriesFrame(main)
    categoriesFrame.grid(row=5, column=1, sticky=tk.E)

    descriptionFrame, _ = makeDescriptionFrame(main)
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

    classificationFrame, _ = makeClassificationFrame(informationsFrame)
    classificationFrame.grid(row=0, column=0, sticky=tk.W)

    priorityFrame, _ = makePriorityFrame(informationsFrame)
    priorityFrame.grid(row=0, column=1, sticky=tk.E)

    tranparencyFrame, _ = makeTranspFrame(informationsFrame)
    tranparencyFrame.grid(row=1, column=0, sticky=tk.W)

    geoFrame, _ = makeGeoFrame(informationsFrame)
    geoFrame.grid(row=1, column=1, sticky=tk.E)

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

    def submit():
        # mandatory properties
        summary = None  # not a mandatory property in theory but got no sense withtout it
        if (not summaryDict["value"].get()):
            raise Exception(f"The event has to got a title")
        summary = summaryDict["value"].get()

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


        tmstamp = datetime.now()
        event = Vevent(
            tmstamp,
            dtstart,
            tmstamp
        )
        print(event)

    submitButton.config(
        command=submit
    )
    submitButton2.config(
        command=submit
    )

    return main
    # eventFrame = tk.Frame(masterFrame)
    # eventObject = {"value": None}

    # dtStartFrame, dtStartDict = makeDtFrame(eventFrame, configuration, "start")
    # dtStartFrame.pack(anchor="w")

    # dtendFrame, dtEndDict = makeDtFrame(eventFrame, configuration, "end")
    # dtendFrame.pack(anchor="w")

    # attachmentFrame, attachmentDict = makeAttachmentFrame(eventFrame, configuration)
    # attachmentFrame.pack(anchor="w")

    # categoriesFrame, categoriesDict = makeCategoriesFrame(eventFrame, configuration)
    # categoriesFrame.pack(anchor="w")

    # classificationFrame, classificationDict = makeClassificationFrame(eventFrame, configuration)
    # classificationFrame.pack(anchor="w")

    # commentFrame, commentDict = makeCommentFrame(eventFrame, configuration)
    # commentFrame.pack(anchor="w")

    # descriptionFrame, descriptionDict = makeDescriptionFrame(eventFrame, configuration)
    # descriptionFrame.pack(anchor="w")

    # geoFrame, geoDict = makeGeoFrame(eventFrame, configuration)
    # geoFrame.pack(anchor="w")

    # locationFrame, locationDict = makeLocationFrame(eventFrame, configuration)
    # locationFrame.pack(anchor="w")
   
    # priorityFrame, priorityDict = makePriorityFrame(eventFrame)
    # priorityFrame.pack(anchor="w")

    # resourceFrame, resourceDict = makeResourceFrame(eventFrame, configuration)
    # resourceFrame.pack(anchor="w")

    # statusFrame, statusDict = makeStatusFrame(eventFrame, configuration, "event")
    # statusFrame.pack(anchor="w")

    # durationFrame, durationDict = makeDurationFrame(eventFrame, configuration)
    # durationFrame.pack(anchor="w")

    # transpFrame, transpDict = makeTranspFrame(eventFrame, configuration)
    # transpFrame.pack(anchor="w")

    # attendeeFrame = makeAttendeeFrame(eventFrame, configuration, "event")
    # attendeeFrame.pack(anchor="w")

    # def createEvent():
    #     tmstmp = datetime.now()

    #     summary = None
    #     if (summaryDict["value"].get() != ""):
    #         summary = Summary(summaryDict["value"].get(), summaryDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], summaryDict["language"].get()))
    #     else:
    #         raise Exception(f"An event has to show a title, please put a title")

    #     dtstart = None
    #     if (dtStartDict["date-status"].get()):
    #         truc = dtStartDict["date"].get().split('/')
    #         dtstart = datetime.strptime(f"{truc[0]}-{truc[1]}-{truc[2]}", "%Y-%m-%d")
    #         if (dtStartDict["time-status"].get()):
    #             dtstart = dtstart.replace(
    #                 hour=int(dtStartDict["hour"].get()),
    #                 minute=int(dtStartDict["minute"].get()),
    #                 second=int(dtStartDict["second"].get())
    #             )

    #     dtend = None
    #     if (dtEndDict["date-status"].get()):
    #         truc = dtEndDict["date"].get().split('/')
    #         dtend = datetime.strptime(f"{truc[0]}-{truc[1]}-{truc[2]}", "%Y-%m-%d")
    #         if (dtEndDict["time-status"].get()):
    #             dtend = dtend.replace(
    #                 hour=int(dtEndDict["hour"].get()),
    #                 minute=int(dtEndDict["minute"].get()),
    #                 second=int(dtEndDict["second"].get())
    #             )

    #     categories = None
    #     if (categoriesDict["state"].get() and len(categoriesDict["listbox"].curselection()) > 0):
    #         categories = Categories([categoriesDict["listbox"].get(index) for index in categoriesDict["listbox"].curselection()])

    #     attachment = None
    #     if (attachmentDict["state"].get()):
    #         attachment = Attachement(attachmentDict["value"].get(), typename=attachmentDict["fmttype"]["type"].get(), subtypename=attachmentDict["fmttype"]["subtype"].get())

    #     classification = None
    #     if (classificationDict["state"].get()):
    #         classification = Classification(classificationDict["value"].get())

    #     comment = None
    #     if (commentDict["state"].get()):
    #         comment = Comment(commentDict["value"].get("1.0", "end-1c"), commentDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], commentDict["language"].get()))

    #     description = None
    #     if (descriptionDict["state"].get()):
    #         description = Description(descriptionDict["value"].get("1.0", "end-1c"), descriptionDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], descriptionDict["language"].get()))
    #     
    #     geo = None
    #     if (geoDict["state"].get()):
    #         geo = Geo(float(geoDict["lat"].get()), (geoDict["long"].get()))

    #     location = None
    #     if (locationDict["state"].get()):
    #         location = Location(locationDict["value"].get(), locationDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], locationDict["language"].get()))

    #     priority = None
    #     if (priorityDict["state"].get()):
    #         priority = Priority(int(priorityDict["value"].get()))

    #     # TODO: check why stringify doesn't work
    #     resource = None
    #     if (resourceDict["state"].get()):
    #         resource = Resources(resourceDict["value"].get("1.0", "end-1c"), resourceDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], resourceDict["language"].get()))

    #     status = None
    #     if (statusDict["state"].get()):
    #         status = Status(statusDict["value"].get())

    #     transp = None
    #     if (transpDict["state"].get()):
    #         transp = Transparency(transpDict["value"].get())

    #     duration = None
    #     if (durationDict["value"].get()):
    #         duration = Duration(
    #             int(durationDict["week"].get()),
    #             int(durationDict["day"].get()),
    #             int(durationDict["hour"].get()),
    #             int(durationDict["minute"].get()),
    #             int(durationDict["second"].get())
    #         )

    #     end = None
    #     if (dtend and duration):
    #         raise Exception(f"Can't have an end date and a duration")
    #     elif (not dtend and not duration):
    #         raise Exception(f"An event has to got an end")
    #     else:
    #         if (not dtend):
    #             end = duration
    #         else:
    #             end = dtend

    #     event = Vevent(
    #         tmstmp,
    #         dtstart=dtstart,
    #         end=end,
    #         classification=classification,
    #         description=description,
    #         attach=attachment,
    #         categories=categories,
    #         comment=comment,
    #         geo=geo,
    #         location=location,
    #         priority=priority,
    #         # resources=[resource],
    #         status=status,
    #         title=summary,
    #         transp=transp
    #     )
    #     print(event)
    #     eventObject["value"] = event


    # addButton = tk.Button(eventFrame, text="Add event", command=createEvent)
    # addButton.pack(anchor="w")

    # return eventFrame, eventObject