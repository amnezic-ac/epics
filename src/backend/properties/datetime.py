from src.backend.properties.property import *
from src.backend.datatypes import DurationType
from src.backend.parameters import Fbtype

class Duration(Property):
    def __init__(self, week: int = 0, day: int = 0, hour: int = 2, minute: int = 0, second: int = 0):
        self.value = DurationType(week, day, hour, minute, second)

    def __str__(self):
        return f"DURATION:{str(self.value)}"

class Transparency(Property):
    # not displayed on thunderbird
    def __init__(self, value: str = "OPAQUE"):
        if (value not in ["OPAQUE", "TRANSPARENT"]):
            raise Exception(f"Transparency property can only take OPAQUE o TRANSPARENT value, actual value: {value}")

        self.value = value

    def __str__(self):
        return f"TRANSP:{self.value}"

class Freebusytime(Property):
    def __init__(self, period: Period, status: str):
        self.period = period
        self.status = Fbtype(status)

    def __str__(self):
        return f"DURATION;{self.status}:{str(self.period)}"