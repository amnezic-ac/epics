from parameters.description import Categories, Classification, Comment, Description, Geo, Location, Priority, Resources, Status, Summary

class Vevent():
    # for further information, please refer to 3.6.1

    uid = 1

    def __init__(self, categories: [str] = None, classification: str = None, comment: str = None, description: str = None, geo: (float, float) = None, location: str = None, priority: int = None, resources: str = None, status: str = None, summary: str = None, attendee: str = None, contact: str = None, organizer: str = None, recurrid: str = None, relatedto: str = None, url: str = None, exdate: str = None, rdate: str = None, rrule: str = None):
        self.uid = Vevent.uid
        Vevent.uid += 1

        if (categories):
            self.categories = Categories(categories)
        else:
            self.categories = None

        self.classification = classification
        self.comment = comment
        self.description = description

        if (geo):
            self.geo = Geo(geo[0], geo[1])
        else:
            self.geo = None

        self.location = location

        if (self.priority):
            self.priority = priority
        else:
            self.priority = None

        self.resources = None
        self.status = None
        self.summary = None
        self.attendee = attendee
        self.contact = contact
        self.organizer = organizer
        self.recurrid = recurrid
        self.relatedto = relatedto
        self.url = url
        self.exdate = exdate
        self.rdate = rdate
        self.rrule = rrule