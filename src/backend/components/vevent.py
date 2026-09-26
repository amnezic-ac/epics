from src.properties import Uid, Categories, Classification, Comment, Description, Geo, Location, Priority, Resources, Status, Summary, Dtend, Dtstart, Duration, Transparency, Attachement, Atttendee, Comment, Contact
from src.components.component import Component
from datetime import datetime, timedelta

class Vevent(Component):
    # for further information, please refer to 3.6.1

    # TODO:
    """
    - tester d'avoir plusieurs comments
    """
    def __init__(self,
        dtstamp: datetime,
        dtstart: datetime,
        end: datetime|Duration,
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
        title: Summary = None,
        transp: Transparency = None,
        attach: [Attachement] = None,
        attendee: [Atttendee] = None,
        categories: Categories = None,
        comment: [Comment] = None,
        contact: [Contact] = None,
        resources: [Resources] = None
        ):
        ### mandatory
        self.dtstamp = dtstamp
        self.uid = Uid(f"{self.dtstamp.strftime("%Y%m%dT%zZ")}")
        self.dtstart = dtstart

        self.dtend = None
        if (type(end) is datetime):
            self.dtend = end
        if (type(end) is Duration):
            self.dtend = self.dtstart + timedelta(weeks=end.value.week, days=end.value.day, hours=end.value.hour, minutes=end.value.minute, seconds=end.value.second)

        ### once maximum
        self.classification = classification
        self.created = created
        self.description = description
        self.geo = geo
        self.lastmod = lastmod
        self.location = location
        self.organizer = organizer
        self.priority = priority
        self.status = status
        self.summary = title
        self.transp = transp

        ### may occur more than once
        self.attach = attach
        self.attendee = attendee
        self.categories = categories
        self.comment = comment
        self.contact = contact
        self.resources = resources

        ### TODO: seq, url, recurid, rrule, exdate, rstatus, related, rdate



    def __str__(self):
        return super().__str__("VEVENT")