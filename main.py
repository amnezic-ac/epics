from src.components.calendar import Calendar
from src.components.vevent import Vevent
from src.properties import *

def main():
    cal = Calendar()

    my_event = Vevent(["work", "link"])
    cal.add_component(my_event)

    print(cal)




main()