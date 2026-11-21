from src.backend.properties.property import *

DEFAULT_DURATION_HOUR = configuration["duration"]["default_hour_duration"]

class Duration(Property):
    def __init__(self, week: int = 0, day: int = 0, hour: int = DEFAULT_DURATION_HOUR, minute: int = 0, second: int = 0):
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
    def __init__(self, status: str = "BUSY", week: int = 0, day: int = 0, hour: int = DEFAULT_DURATION_HOUR, minute: int = 0, second: int = 0):
        self.value = Duration(week, day, hour, minute, second)
        self.status = Fbtype(status)

    def __str__(self):
        return f"DURATION;{str(self.status)}:{str(self.value)}"