from tkinter import ttk
import tkinter as tk
from datetime import datetime, timedelta

from src.backend.components.vevent import Vevent
from src.backend.properties import *
from src.gui.properties import *

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

def makeEventFrame(root: tk.Frame, eventHolder: dict, configuration: dict) -> tk.Frame:
    frame = tk.Frame(root)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    for i in range(10):
        frame.rowconfigure(i, weight=1)

    # title and classification
    titleHolder = {}
    titleFrame = makeSummaryFrame(frame, titleHolder, configuration["language"])
    # to be able to display the title in real time
    eventHolder["titleEntry"] = titleHolder["titleEntry"]
    titleFrame.grid(row=0, column=0, sticky=[tk.W])

    classificationHolder = {}
    classificationFrame = makeClassificationFrame(frame, classificationHolder, configuration["classification"])
    classificationFrame.grid(row=0, column=1, sticky=[tk.W])

    # start, end and duration
    dtStartHolder = {}
    dtStartFrame = makeDtFrame(frame, "start", dtStartHolder)
    dtStartFrame.grid(row=1, rowspan=2, column=0, sticky=[tk.W])

    dtEndHolder = {}
    dtEndFrame = makeDtFrame(frame, "end", dtEndHolder)
    dtEndFrame.grid(row=1, rowspan=2, column=1, sticky=[tk.W])

    # location and priority
    locationHolder = {}
    locationFrame = makeLocationFrame(frame, locationHolder, configuration["language"])
    locationFrame.grid(row=5, column=0, sticky=[tk.W])

    priorityHolder = {}
    priorityFrame = makePriorityFrame(frame, priorityHolder, configuration["priority"])
    priorityFrame.grid(row=4, column=2, sticky=[tk.W])

    # categories
    categoriesHolder = {}
    categoriesFrame = makeCategoriesFrame(frame, categoriesHolder, configuration["categories"])
    categoriesFrame.grid(row=5, column=0, columnspan=2, sticky=[tk.W])

    # organizer and attendees
    # attachment
    attachmentHolder = {}
    attachmentFrame = makeAttachmentFrame(frame, attachmentHolder)
    attachmentFrame.grid(row=6, column=0, columnspan=2, sticky=[tk.W])

    # description
    descriptionHolder = {}
    descriptionFrame = makeCommentOrDescriptionFrame(frame, descriptionHolder, "description", configuration["language"])
    descriptionFrame.grid(row=7, column=0, columnspan=2, sticky="nsew")
    # optional
        # rrule
        # transp and geo
        # status
        # url
        # comment
    # cancel and confirm
    cancelButton = tk.Button(frame, text="Cancel")
    cancelButton.grid(row=9, column=0)
    def createEvent():
        now = datetime.now()
        eventHolder["value"] = Vevent(
            now,
            dtstart=dtStartHolder["getValue"](),
            end=dtEndHolder["getValue"](),
            classification=classificationHolder["getValue"](),
            created=None,
            description=descriptionHolder["getValue"](),
            geo=None,
            lastmod=None,
            location=locationHolder["getValue"](),
            organizer=None,
            priority=priorityHolder["getValue"](),
            seq=None,
            status=None,
            title=titleHolder["getValue"](),
            transp=None,
            attach=attachmentHolder["getValue"](),
            attendee=None,
            categories=categoriesHolder["getValue"](),
            comment=None,
            contact=None,
            resources=None,
            url=None
        )
    confirmButton = tk.Button(frame, text="Confirm", command=createEvent)
    confirmButton.grid(row=9, column=1)

    return frame