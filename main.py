from src.components.calendar import Calendar
from src.components.vevent import Vevent
from src.properties import *
from datetime import timedelta

def main():
    cal = Calendar()

    tmp_stamp = datetime.now()
    my_event = Vevent(tmp_stamp, tmp_stamp, datetime(2026, 9, 19, 12, 30))
    my_event.summary = Summary("summary test") # appears as title on thunderbird
    my_event.attendee = [Atttendee("Paul", roleparam="President", rsvpparam=True), Atttendee("Arthur", roleparam="Member", rsvpparam=False)]
    my_event.comment = [Comment("Comment test", language="ch"), Comment("deuxieme comment test")]

    # # my_event = Vevent(tmp_stamp, tmp_stamp, Duration())
    # # my_event.classification = Classification("PUBLIC") # don't display on thunderbird
    # # my_event.geo = Geo(1.59, 6.7) # don't display on thunderbird
    # # my_event.priority = Priority(2) # don't display on thunderbird
    # # my_event.status = Status("status test") # don't display on thunderbird
    # # my_event.transp = Transparency() # don't display on thunderbird
    # my_event.description = Description("description test", language="fr")
    # my_event.lastmod = datetime.now()
    # my_event.location = Location("Le bariole")
    # my_event.organizer = Organizer("Joseph", "Jo")
    # my_event.attach = [Attachement("attachement test"), Attachement("attachement test 2")] # don't display on thunderbird
    # my_event.categories = Categories(["Work", "Sport"])
    # my_event.contact = Contact("contact test")
    # my_event.resources = Resources("ressource test")

    cal.add_component(my_event)
    print(cal)

main()