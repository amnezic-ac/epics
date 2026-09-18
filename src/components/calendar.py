from vevent import Vevent
from valarm import Valarm
from vfreebusy import Vfreebusy
from vjournal import Vjournal
from vtimezone import Vtimezone
from vtodo import Vtodo

class Calendar():

    def __init__(self, uid: str = "uid"):
        self.components = []

    def __str__(self):
        result = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:epics\n"
        # adding the components
        for component in self.components:
            result += f"{component}\n"

        result += "END:VEVENT\nEND:VCALENDAR"

        return result

    def add_component(component):
        self.components.append(component)