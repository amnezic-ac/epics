from src.properties import Categories, Classification, Comment, Description, Geo, Location, Priority, Resources, Status, Summary, Dtend, Dtstart, Duration, Transparency, Attachement, Atttendee, Comment, Contact
from src.components.component import Component
from datetime import datetime

class Vevent(Component):
    # for further information, please refer to 3.6.1
    def __init__(self,
        dtstamp: datetime = datetime.now(),
        dtstart: datetime = datetime.now(),
        classification: Classification = None,
        created: datetime = None,
        description: Description = None,
        geo: Geo = None,
        lastmod: datetime = None,
        location: Location = None,
        organizer: Organizer = None,
        priority: Priority = None,
        seq: str = None,
        status: Status = None,
        summary: Summary = None,
        transp: Transparency = None,
        attach: Attachement = None
        ):
        self.uid = super().uid
        self.dtstamp = dtstamp
        self.dtstart = dtstart
        self.classification = classification
        self.created = created
        self.description = Description
        self.geo = geo

        # not sure about this one
        self.lastmod = lastmod

        self.location = location
        self.organizer = organizer
        self.priority = priority

        # TODO
        self.seq = seq

        self.status = status
        self.summary = summary
        self.transp = transp

        self.attach = attach



    def __str__(self):
        return super().__str__("VEVENT")