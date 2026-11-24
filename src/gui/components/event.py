from src.gui.imports import *
from datetime import datetime, timedelta
from src.backend.components.vevent import Vevent
import uuid

from src.gui.properties.descriptive import makeSummaryFrame, makeClassificationFrame, makeLocationFrame, makePriorityFrame, makeCategoriesFrame, makeAttachmentFrame, makeDescriptionFrame, makeResourceFrame
from src.gui.properties.datetime import makeDtFrame
from src.gui.properties.recurrence import makeRruleFrame
from src.gui.properties.relationship import makeAttendeeFrame, makeOrganizerFrame, makeURLFrame
from src.backend.datatypes import MyDateTime


def makeEventFrame(root: tk.Frame, eventHolder: dict, calId: uuid) -> tk.Frame:
    id_ = uuid.uuid4()
    logging.debug(f"[Event {id_}] User opened a new event frame from {calId} calendar")
    frame = tk.Frame(root)

    # title and classification
    titleHolder = {}
    titleFrame = makeSummaryFrame(frame, titleHolder, id_)
    # to be able to display the title in real time
    eventHolder["titleEntry"] = titleHolder["titleEntry"]
    titleFrame.grid(row=0, column=0, sticky=(tk.W, tk.N))

    classificationHolder = {}
    classificationFrame = makeClassificationFrame(frame, classificationHolder, id_)
    classificationFrame.grid(row=0, column=1, sticky=(tk.W, tk.N))

    # start, end and duration
    dtStartHolder = {}
    dtStartFrame = makeDtFrame(frame, "start", dtStartHolder, id_)
    dtStartFrame.grid(row=1, rowspan=2, column=0, sticky=[tk.W])

    dtEndHolder = {}
    dtEndFrame = makeDtFrame(frame, "end", dtEndHolder, id_)
    dtEndFrame.grid(row=1, rowspan=2, column=1, sticky=[tk.W])

    timestate = tk.BooleanVar(value=configuration["general"]["timestate"])
    timestateText = tk.StringVar(value="Remove time")
    if (timestate.get()):
        dtStartHolder["addTime"]()
        dtEndHolder["addTime"]() 
    else:
        dtStartHolder["removeTime"]()
        dtEndHolder["removeTime"]()
        timestateText.set("Include time")

    def toggleTime():
        actual = not timestate.get()
        if (actual):
            dtStartHolder["addTime"]()
            dtEndHolder["addTime"]() 
            timestateText.set("Remove time")
        else:
            dtStartHolder["removeTime"]()
            dtEndHolder["removeTime"]()
            timestateText.set("Include time")
        timestate.set(actual)
    timeButton = tk.Button(frame, textvariable=timestateText, command=toggleTime)
    timeButton.grid(row=4, column=0, columnspan=2)

    # location and priority
    locationHolder = {}
    locationFrame = makeLocationFrame(frame, locationHolder, id_)
    locationFrame.grid(row=5, column=0, sticky=[tk.W])

    priorityHolder = {}
    priorityFrame = makePriorityFrame(frame, priorityHolder, id_)
    priorityFrame.grid(row=5, column=1, sticky=[tk.W])

    # categories
    categoriesHolder = {}
    categoriesFrame = makeCategoriesFrame(frame, categoriesHolder, id_)
    categoriesFrame.grid(row=6, column=0, columnspan=2, sticky=[tk.W])

    # organizer and attendees
    # attachment
    attachmentHolder = {}
    attachmentFrame = makeAttachmentFrame(frame, attachmentHolder, id_)
    attachmentFrame.grid(row=7, column=0, columnspan=2, sticky=[tk.W])

    # description
    descriptionHolder = {}
    descriptionFrame = makeDescriptionFrame(frame, descriptionHolder, id_)
    descriptionFrame.grid(row=8, column=0, columnspan=2, sticky="nsew")
    # optional
        # rrule
        # transp and geo
        # status
        # url
        # comment
    resourcesHolder = {}
    resourcesFrame = makeResourceFrame(frame, resourcesHolder, id_)
    resourcesFrame.grid(row=9, column=0)
    # cancel and confirm
    cancelButton = tk.Button(frame, text="Cancel")
    cancelButton.grid(row=10, column=0)
    def createEvent():
        logging.debug(f"[Event {id_}] User clicked on confirm or modify button")
        now = datetime.now()
        try:
            event = Vevent(
                datetime.now(),
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
            logging.debug(f"[Event {id_}] User successfully created {titleHolder["getValue"]()} event")
            print(event)
            return event
        except:
            logging.error(f"[Event {id_}] Unable to create {id_} event")
            return None
    eventHolder["getValue"] = createEvent
    confirmButton = tk.Button(frame, text="Check the event")
    confirmButton.grid(row=9, column=1)

    return frame