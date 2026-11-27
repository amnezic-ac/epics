from src.gui.imports import *
from datetime import datetime, timedelta
from src.backend.components.vevent import Vevent
import uuid

from src.gui.properties.descriptive import *
from src.gui.properties.datetime import *
from src.gui.properties.recurrence import makeRruleFrame
from src.gui.properties.relationship import makeAttendeeFrame, makeOrganizerFrame, makeURLFrame
from src.backend.datatypes import MyDateTime


def makeEventFrame(root: tk.Frame, eventHolder: dict, calId: uuid) -> tk.Frame:
    id_ = uuid.uuid4()
    logging.debug(f"[Event {id_}] User opened a new event frame from {calId} calendar")
    frame = tk.Frame(root)
    propertiesHolder = {}

    # title and classification
    titleFrame = makeSummaryFrame(frame, propertiesHolder, id_)
    # to be able to display the title in real time
    eventHolder["titleEntry"] = propertiesHolder["titleEntry"]
    titleFrame.grid(row=0, column=0, sticky=(tk.W, tk.N))

    classificationFrame = makeClassificationFrame(frame, propertiesHolder, id_)
    # classificationFrame.grid(row=0, column=1, sticky=(tk.W, tk.N))

    # start, end and duration
    dtStartFrame = makeDtFrame(frame, "start", propertiesHolder, id_)
    dtStartFrame.grid(row=1, rowspan=2, column=0, sticky=[tk.W, tk.N])

    dtEndFrame = makeDtFrame(frame, "end", propertiesHolder, id_)
    dtEndFrame.grid(row=1, column=3, sticky=[tk.W])

    durationFrame = makeDurationFrame(frame, propertiesHolder, id_)
    durationFrame.grid(row=2, column=3)

    # let the user choose between datetime and duration
    endMode = tk.StringVar(value=configuration["general"]["endtype"])
    def toggleEnd():
        if (endMode.get() == "datetime"):
            durationFrame.grid_remove()
            dtEndFrame.grid()
        else:
            durationFrame.grid()
            dtEndFrame.grid_remove()
    toggleEnd()

    dtendButton = ttk.Radiobutton(frame, text="to ", value="datetime", variable=endMode, command=toggleEnd)
    dtendButton.grid(row=1, column=2)
    durationButton = ttk.Radiobutton(frame, text="for ", value="duration", variable=endMode, command=toggleEnd)
    durationButton.grid(row=2, column=2)


    timestate = tk.BooleanVar(value=configuration["general"]["timestate"])
    timestateText = tk.StringVar(value="Remove time")
    def toggleTime():
        actual = not timestate.get()
        if (actual):
            propertiesHolder["start-addTime"]()
            propertiesHolder["end-addTime"]() 
            propertiesHolder["addTime"]()
            timestateText.set("Remove time")
        else:
            propertiesHolder["start-removeTime"]()
            propertiesHolder["end-removeTime"]()
            propertiesHolder["removeTime"]()
            timestateText.set("Include time")
        timestate.set(actual)
    toggleTime()

    timeButton = tk.Button(frame, textvariable=timestateText, command=toggleTime)
    timeButton.grid(row=4, column=0, columnspan=2)

    # location and priority
    locationFrame = makeLocationFrame(frame, propertiesHolder, id_)
    # locationFrame.grid(row=5, column=0, sticky=[tk.W])

    priorityFrame = makePriorityFrame(frame, propertiesHolder, id_)
    # priorityFrame.grid(row=5, column=1, sticky=[tk.W])

    # categories
    categoriesFrame = makeCategoriesFrame(frame, propertiesHolder, id_)
    # categoriesFrame.grid(row=6, column=0, columnspan=2, sticky=[tk.W])

    # organizer and attendees
    # attachment
    attachmentFrame = makeAttachmentFrame(frame, propertiesHolder, id_)
    # attachmentFrame.grid(row=7, column=0, columnspan=2, sticky=[tk.W])

    # description
    descriptionFrame = makeDescriptionFrame(frame, propertiesHolder, id_)
    # descriptionFrame.grid(row=8, column=0, columnspan=2, sticky=(tk.W))
    # optional
        # rrule
        # transp and geo
    transpFrame = makeTranspFrame(frame, propertiesHolder, id_)
    transpFrame.grid(row=10, column=0)
    geoFrame = makeGeoFrame(frame, propertiesHolder, id_)
    # geoFrame.grid(row=12, column=0)
        # status
    statusFrame = makeStatusFrame(frame, propertiesHolder, "event", id_)
    # statusFrame.grid(row=5, column=0)
        # url
        # comment
    commentFrame = makeCommentFrame(frame, propertiesHolder, id_)
    # commentFrame.grid(row=13, column=0)

    fbtFrame = makeFreeBusyFrame(frame, propertiesHolder, id_)
    fbtFrame.grid(row=13, column=0, columnspan=3)

    resourcesFrame = makeResourceFrame(frame, propertiesHolder, id_)
    # resourcesFrame.grid(row=15, column=0)
    # cancel and confirm
    cancelButton = tk.Button(frame, text="Cancel")
    cancelButton.grid(row=16, column=0)
    def createEvent():
        logging.debug(f"[Event {id_}] User clicked on confirm or modify button")
        now = datetime.now()
        try:
            end = None
            if (endMode.get() == "datetime"):
                end = propertiesHolder["end-getDt"]()
            else:
                end = propertiesHolder["getDuration"]()

            event = Vevent(
                now,
                title=propertiesHolder["getSummary"](),
                dtstart=propertiesHolder["start-getDt"](),
                end=end,
                classification=propertiesHolder["getClassification"](),
                created=now,
                description=propertiesHolder["getDescription"](),
                geo=propertiesHolder["getGeo"](),
                lastmod=now,
                location=propertiesHolder["getLocation"](),
                organizer=None,
                priority=propertiesHolder["getPriority"](),
                seq=None,
                status=propertiesHolder["getStatus"](),
                transp=propertiesHolder["getTransp"](),
                attach=propertiesHolder["getAttachment"](),
                attendee=None,
                categories=propertiesHolder["getCategories"](),
                comment=propertiesHolder["getComment"](),
                contact=None,
                resources=propertiesHolder["getResources"](),
                url=None
            )
            logging.debug(f"[Event {id_}] User successfully created {propertiesHolder["titleEntry"].get()} event")
            print(event)
            return event
        except:
            logging.error(f"[Event {id_}] Unable to create {id_} event")
            return None
    eventHolder["getValue"] = createEvent
    confirmButton = tk.Button(frame, text="Check the event")
    confirmButton.grid(row=9, column=1)

    return frame