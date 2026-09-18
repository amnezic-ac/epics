from src.components.calendar import Calendar
from src.components.vevent import Vevent
from src.properties import *

def main():
    cal = Calendar()

    my_event = Vevent()
    my_event.classification = Classification("PUBLIC") # don't display on thunderbird
    my_event.description = Description("description test", language="fr")
    my_event.geo = Geo(1.59, 6.7) # don't display on thunderbird
    my_event.lastmod = datetime.now()
    my_event.location = Location("Le bariole")
    my_event.organizer = Organizer("Joseph", "Jo")
    my_event.priority = Priority(2) # don't display on thunderbird
    my_event.status = Status("status test") # don't display on thunderbird
    my_event.summary = Summary("summary test") # appears as title on thunderbird
    my_event.transp = Transparency() # don't display on thunderbird
    my_event.attach = Attachement("attachement test") # don't display on thunderbird

    cal.add_component(my_event)

    print(cal)

main()