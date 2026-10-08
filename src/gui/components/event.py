from tkinter import ttk
import tkinter as tk
from datetime import datetime, timedelta

from src.backend.components.vevent import Vevent
from src.backend.properties import *
from src.gui.properties import *
from src.utils import logging, configuration

# TODO
"""
- organizer
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

def makeEventFrame(root: tk.Frame, eventHolder: dict) -> tk.Frame:
    """
    create a frame that will handle VEVENT component creation

    Params:
    ------
    - root: tk.Frame
        parent frame of the newly created frame with all the vevent properties
    - eventHolder: dict
        value holder for the event with only one field: "value"

    Returns:
    -------
    - tk.Frame: the newly created frame (note: needs to be packed after the return of the function)
    """
    frame = ttk.Frame(root)
    logging.debug(f"New event tab created")

    title = tk.StringVar(value="")
    # mandatory properties
    summaryFrame, summaryDict = makeSummaryFrame(frame, title)
    dtStartFrame, dtStartDict = makeDtFrame(frame, "start")

    endFrame = tk.Frame(frame)
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
        pass
        durationUsed.set(True)
        durationFrame.grid(row=1, column=1)
        if (dtendFrame):
            dtendFrame.grid_forget()
    durationButton = ttk.Radiobutton(endFrame, text="Duration", value="duration", variable=endChoice, command=toggleDurationFrame)
    durationButton.grid(row=1, column=0, sticky=tk.W)

    # optional but must not occur more than once
    classificationFrame, classificationDict = makeClassificationFrame(frame)
    # created
    descriptionFrame, descriptionDict = makeDescriptionFrame(frame)
    geoFrame, geoDict = makeGeoFrame(frame)
    # last-mod
    locationFrame, locationDict = makeLocationFrame(frame)
    organizerFrame, organizerListbox = makeAttendeeFrame(frame, "event", "Organizer: ")
    priorityFrame, priorityDict = makePriorityFrame(frame)
    # seq
    statusFrame, statusValue = makeStatusFrame(frame, "event")
    tranparencyFrame, transpDict = makeTranspFrame(frame)
    urlFrame, urlValue = makeURLFrame(frame)
    # recurid

    # optional but should not occur more than once
    # rrule

    # optional and may occur more than once
    attachmentFrame, attachmentDict = makeAttachmentFrame(frame)
    attendeesFrame, attendeesListbox = makeAttendeeFrame(frame, "event", "Attendees: ")
    categoriesFrame, categoriesDict = makeCategoriesFrame(frame)
    commentFrame, commentDict = makeCommentFrame(frame)
    # contact
    # exdate
    # rstatus
    # related
    # resources
    # rdate

    # user actions buttons
    destroyButton = tk.Button(frame, text="Cancel this event")
    label = tk.Label(frame, text="Show more ?")
    submitButton = tk.Button(frame, text="Confirm")

    # general frame grid arrangement
    for row in range(13):
        frame.rowconfigure(row, weight=1)
    for col in range(6):
        frame.columnconfigure(col, weight=1)

    summaryFrame.grid(row=0, column=0,sticky=tk.W, columnspan=3)
    statusFrame.grid(row=0, column=3, sticky=tk.E, columnspan=3) # it should not be RSVP ?

    dtStartFrame.grid(row=1, column=0, sticky=tk.W, columnspan=3)
    endFrame.grid(row=1, column=3, sticky=tk.E, columnspan=3)
    
    descriptionFrame.grid(row=2, column=0, sticky=tk.W, columnspan=3)
    categoriesFrame.grid(row=2, column=3, sticky=tk.E, columnspan=3)

    organizerFrame.grid(row=3, column=0, sticky=tk.NW, columnspan=3)
    fixme = tk.StringVar(value="FIXME")
    ttk.Entry(frame, textvariable=fixme).grid(row=4, column=0, sticky=tk.NW, columnspan=3)
    attendeesFrame.grid(row=3, column=3, rowspan=2, columnspan=3, sticky=tk.NE)

    locationFrame.grid(row=5, column=0, columnspan=6, sticky=tk.NSEW)
    attachmentFrame.grid(row=6, column=0, sticky=tk.W, columnspan=6)

    destroyButton.grid(row=7, column=0, sticky=tk.W, columnspan=2)
    label.grid(row=7, column=2, sticky=tk.W, columnspan=2)
    submitButton.grid(row=7, column=4, sticky=tk.E, columnspan=2)

    # additional infos
    classificationFrame.grid(row=8, column=0, columnspan=3, sticky=tk.W)
    classificationFrame.grid_forget()
    priorityFrame.grid(row=8, column=3, columnspan=3, sticky=tk.E)
    priorityFrame.grid_forget()

    tranparencyFrame.grid(row=9, column=0, columnspan=3, sticky=tk.W)
    tranparencyFrame.grid_forget()
    geoFrame.grid(row=9, column=3, columnspan=3, sticky=tk.E)
    geoFrame.grid_forget()

    urlFrame.grid(row=10, column=0, columnspan=6, sticky=tk.W)
    urlFrame.grid_forget()
    commentFrame.grid(row=11, column=0, columnspan=6, sticky=tk.NSEW)
    commentFrame.grid_forget()
    

    state = tk.BooleanVar(value=False)
    def toggleHiddableFrame(event):
        actual = not state.get()
        if (actual):
            classificationFrame.grid()
            priorityFrame.grid()
            tranparencyFrame.grid()
            geoFrame.grid()
            urlFrame.grid()
            commentFrame.grid()
            destroyButton.grid(row=12, column=0, columnspan=2, sticky=tk.W)
            label.grid(row=12, column=2, columnspan=4)
            label.config(text="Show less informations")
            submitButton.grid(row=12, column=4, columnspan=2, sticky=tk.E)
            logging.debug(f"{summaryDict["value"].get()} event frame displayed hiddable properties")
        else:
            classificationFrame.grid_forget()
            priorityFrame.grid_forget()
            tranparencyFrame.grid_forget()
            geoFrame.grid_forget()
            urlFrame.grid_forget()
            commentFrame.grid_forget()
            destroyButton.grid(row=7, column=0, columnspan=2, sticky=tk.W)
            label.grid(row=7, column=2, columnspan=4)
            label.config(text="Show more informations")
            submitButton.grid(row=7, column=4, columnspan=2, sticky=tk.E)
            logging.debug(f"{summaryDict["value"].get()} event frame hidded hiddable properties")
        state.set(actual)
    label.bind('<Double-1>', toggleHiddableFrame)

    def destroy():
        logging.debug(f"User destroyed {summaryDict["value"].get()} event")
        eventHolder["value"] = None
        frame.destroy()
    destroyButton.config(command=destroy)

    submitState = tk.BooleanVar(value=False)
    def submit():
        if (not submitState.get()):
            logging.debug(f"User attempt to create {title.get()} event")
        else:
            logging.debug(f"User attempt to modify {title.get()} event")
        # mandatory properties
        summary = None  # not a mandatory property in theory but got no sense withtout it
        if (not summaryDict["value"].get()):
            logging.warning(f"The event has no title")
            raise Exception(f"The event has to got a title")
        summary = Summary(summaryDict["value"].get())

        dtstart = None
        if (not dtStartDict["date"].get()):
            logging.warning(f"{title.get()} event has no start date")
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

        # optional properties
        categories = None
        categoriesLength = len(categoriesDict["listbox"].curselection())
        if (categoriesLength > 0):
            categories = Categories([categoriesDict["listbox"].get(index) for index in categoriesDict["listbox"].curselection()])

        classification = None
        comment = None
        description = None
        if (descriptionDict["value"].get("1.0", "end-1c")):
            description = Description(descriptionDict["value"].get("1.0", "end-1c"), descriptionDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], descriptionDict["language"].get()))

        geo = None
        location = None
        priority = None
        status = None
        transp = None
        url = None
        if (state.get()):

            # attachment = None
            # if (attachmentDict["state"].get()):
            #     attachment = Attachement(attachmentDict["value"].get(), typename=attachmentDict["fmttype"]["type"].get(), subtypename=attachmentDict["fmttype"]["subtype"].get())

            if (classificationDict["value"].get()):
                classification = Classification(classificationDict["value"].get())

            if (commentDict["value"].get("1.0", "end-1c")):
                comment = Comment(commentDict["value"].get("1.0", "end-1c"), commentDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], commentDict["language"].get()))

            
            if (geoDict["lat"].get() and geoDict["long"].get()):
                geo = Geo(float(geoDict["lat"].get()), (geoDict["long"].get()))

            if (locationDict["value"].get("1.0", "end-1c")):
                location = Location(locationDict["value"].get("1.0", "end-1c"), locationDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], locationDict["language"].get()))

            if (priorityDict["value"].get()):
                priority = Priority(int(priorityDict["value"].get()))

            # TODO: check why stringify doesn't work
            # resource = None
            # if (resourceDict["state"].get()):
            #     resource = Resources(resourceDict["value"].get("1.0", "end-1c"), resourceDict["altrep"].get("1.0", "end-1c"), findLangIdFromLangValue(configuration["language"]["choices"], resourceDict["language"].get()))

            if (statusValue.get()):
                status = Status(statusValue.get())

            if (transpDict["value"].get()):
                transp = Transparency(transpDict["value"].get())

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
        eventHolder["value"] = event
        if (not submitState.get()):
            logging.debug(f"\"{title.get()}\" event has successfully been created")
        else:
            logging.debug(f"\"{title.get()}\" event has successfully been modified")
        submitState.set(True)
        submitButton.config(text="Modify")
    submitButton.config(
        command=submit
    )

    return frame