from datetime import datetime
from enum import Enum, auto

DEFAULT_HOUR_DURATION = 2

class Caladress():
    def __init__(self):
        self.value = "ERROR"

    def __str__():
        return self.value

class Uri():
    # refer to RFC 3986
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return self.value

class DurationType():
    def __init__(self, week: int, day: int, hour: int, minute: int, second: int):
        for variable in [week, day, hour, minute, second]:
            if (not (variable >= 0)):
                raise Exception(f"A duration can't be {variable} {variable.__getattribute__.__name__}, needs to be positive.")

        self.week = week
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second

    def __str__(self):
        result = "P"

        if (self.week > 0):
            result += f"{self.week}W"
        if (self.day > 0):
            result += f"{self.day}D"
        if (self.hour > 0 or self.minute > 0 or self.second > 0):
            result += "T"
            if (self.hour > 0):
                result += f"{self.hour}H"
            if (self.minute > 0):
                result += f"{self.minute}M"
            if (self.second > 0):
                result += f"{self.second}S"
        
        return result

class Rrule():
    # cf section 3.3.10
    class Frequence(Enum):
        YEARLY      = 1
        MONTHLY     = auto()
        WEEKLY      = auto()
        DAILY       = auto()
        HOURLY      = auto()
        MINUTELY    = auto()
        SECONDLY    = auto()

    # cf section 3.3.10
    # TODO: re read the specs to make negative values possible
    def __init__(self,
        freq: Frequence,
        until: datetime = None,
        count: int = 0,
        interval: int = None,
        byseclist: [int] = None,
        byminlist: [int] = None,
        byhrlist: [int] = None,
        bywdaylist: [str] = None,
        bymodaylist: [int] = None,
        byyrdaylist: [int] = None,
        bywknolist: [int] = None,
        bymolist: [int] = None,
        bysplit: [int] = None,
        weekday: str = None,
        datetime_format: bool = True # indicate if DTSTART has datetime format or not
    ):
        if (until and count):
            raise Exception(f"Can't take a count and an until")

        self.freq = freq
        self.until = until
        if (count and count <= 0):
            raise Exception(f"Impossible to add a 0 or negative repetition")
        self.count = count
        if (interval and interval <= 0):
            raise Exception(f"Impossible to have a 0 or negative interval")
        self.interval = interval

        self.byseclist = None
        self.byminlist = None
        self.byhrlist = None
        if (datetime_format):
            if (byseclist and any([(value < 0 or value > 60) for value in byseclist])):
                raise Exception(f"There is at least one second value not included between 0 and 60")
            self.byseclist = byseclist
            if (byminlist and any([(value < 0 or value > 59) for value in byminlist])):
                raise Exception(f"There is at least one minute value not included between 0 and 59")
            self.byminlist = byminlist
            if (byhrlist and any([(value < 0 or value > 23) for value in byhrlist])):
                raise Exception(f"There is at least one hour value not included between 0 and 23")
            self.byhrlist = byhrlist

        self.bywdaylist = None
        if (self.freq.value not in [Rrule.Frequence.MONTHLY, Rrule.Frequence.YEARLY]):
            self.bywdaylist = bywdaylist
        if (bymodaylist and any([(value < -31 or value > 31 or value == 0) for value in bymodaylist])):
            raise Exception(f"There is at least one day number of the month value not included between -31 and 31")
        self.bymodaylist = bymodaylist
        if (byyrdaylist and any([(value < -366 or value > 366 or value == 0) for value in byyrdaylist])):
            raise Exception(f"There is at least one day number of the year value not included between 1 and 366")
        self.byyrdaylist = byrdaylist
        if (bywknolist and any([(value < -53 or value > 53 or value == 0) for value in byyrdaylist])):
            raise Exception(f"There is at least one week number of the year value not included between -53 and 53")
        self.bywknolist = bywknolist
        if (bymolist and any([(value < 1 or value > 12) for value in byyrdaylist])):
            raise Exception(f"There is at least one month number of the year value not included between 1 and 53")
        self.bymolist = bymolist
        if (bymolist and any([(value < 1 or value > 12) for value in byyrdaylist])):
            raise Exception(f"There is at least one month number of the year value not included between 1 and 53")
        self.bysplit = bysplit
        if (bysplit and any([(value < -366 or value > 366 or value == 0) for value in byyrdaylist])):
            raise Exception(f"There is at least one month number of the year value not included between -53 and 53")
        self.weekday = weekday


    def __str__(self):
        result = f"RRULE:"
        for attr, value in self.__dict__.items():
            if (not value):
                continue

            result += f"{attr.upper()}="

            if (type(value) is list):
                for i in range(len(value)-1):
                    result += f"{str(value[i]).upper()},"
                result += f"{str(value[-1]).upper()}"
            else:
                result += f"{str(value).upper()}"

            result += f";"

        return result[:-1]