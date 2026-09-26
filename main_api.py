from src.backend.components.calendar import Calendar
from src.backend.components.vevent import Vevent
from src.backend.components.valarm import Valarm
from src.backend.properties import *
from datetime import timedelta

# This is a file showing some example of how this software can be used as a Python API

def main():
    myCalendar = Calendar()
    tmstp = datetime.now()

    # myEvent = Vevent(tmstp, tmstp, tmstp + timedelta(hours=2))
    # myCalendar.add_component(myEvent)

    print(myCalendar)

main()