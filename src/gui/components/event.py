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
    titleFrame.grid()
    # start, end and duration
    # location and priority
    # categories
    # organizer and attendees
    # attachment
    # description
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
            dtstart=now,
            end=now,
            classification=None,
            created=None,
            description=None,
            geo=None,
            lastmod=None,
            location=None,
            organizer=None,
            priority=None,
            seq=None,
            status=None,
            title=titleHolder["getValue"](),
            transp=None,
            attach=None,
            attendee=None,
            categories=None,
            comment=None,
            contact=None,
            resources=None,
            url=None
        )
    confirmButton = tk.Button(frame, text="Confirm", command=createEvent)
    confirmButton.grid(row=9, column=1)

    return frame