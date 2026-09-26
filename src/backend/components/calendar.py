from src.components.vevent import Vevent

class Calendar():

    def __init__(self, uid: str = "uid"):
        self.components = []

    def __str__(self):
        result = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:epics\n"
        # adding the components
        for component in self.components:
            result += f"{component}\n"

        result += "END:VCALENDAR"

        return result

    def add_component(self, component : Component):
        self.components.append(component)