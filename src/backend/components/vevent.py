# from src.backend.properties.alarm import *
# from src.backend.properties.change import *
from src.backend.properties.datetime import Duration, Freebusytime
from src.backend.properties.descriptive import Attachment, Categories, Classification, Comment, Description, Geo, Location, Percent, Priority, Resources, Status, Summary
# from src.backend.properties.recurrence import Rrule
from src.backend.properties.relationship import Atttendee, Contact, Organizer, Url, Uid
# from src.backend.properties.timezone import *
from src.backend.datatypes import MyDateTime

from src.backend.components.component import Component
from datetime import datetime, timedelta
import hashlib

class Vevent(Component):
    def __init__(self,
        dtstamp: datetime,
        dtstart: MyDateTime,
        end: MyDateTime|Duration,
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
        attach: [Attachment] = None,
        attendee: [Atttendee] = None,
        categories: Categories = None,
        comment: [Comment] = None,
        contact: [Contact] = None,
        resources: Resources = None,
        url: Url = None
        ):
        ### mandatory
        self.dtstamp = dtstamp
        text = self.dtstamp.strftime("%Y%m%dT%zZ%H%M%S")
        self.uid = Uid(hashlib.sha1(text.encode('utf-8')).hexdigest())
        self.dtstart = dtstart

        self.dtend = None
        if (type(end) is MyDateTime):
            self.dtend = end
        if (type(end) is Duration):
            self.dtend = MyDateTime(
                self.dtstart.value + timedelta(weeks=end.value.week, days=end.value.day, hours=end.value.hour, minutes=end.value.minute, seconds=end.value.second),
                dttype="end",
                gotTime=dtstart.gotTime
            )

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
        self.url = url

        ### TODO: seq, recurid, rrule, exdate, rstatus, related, rdate



    def __str__(self):
        return super().__str__("VEVENT")