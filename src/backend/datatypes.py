from datetime import datetime
from enum import Enum, auto
import re

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
    # TODO: re read the specs to make negative values possible
    def __init__(self,
        freq: str,
        until: datetime = None,
        count: int = None,
        interval: int = 1,
        bysecond: [int] = None,
        byminute: [int] = None,
        byhour: [int] = None,
        byday: [str] = None,
        bymonthday: [int] = None,
        byyearday: [int] = None,
        byweekno: [int] = None,
        bymonth: [int] = None,
        bysetpos: [int] = None,
        wkst: str = "MO",
        datetime_format: bool = True # indicate if DTSTART has datetime format or not
    ):
        """
        create the rrule property object

        Params:
        ------
        - freq: str ["SECONDLY", "MINUTELY", "HOURLY", "DAILY", "WEEKLY", "MONTHLY", "YEARLY"]
            indicate the regularity scale of the component
        - until: datetime
            indicate when the repetition ends
        - count: int
            specify the number of repetition of the event
        - interval: int
            space the component repetition by _interval_ _freq_
        - byXXXX: [int]
            specify the number of the moment of repetition of the event inside a _freq_ time period
        - byday: [str]
            specify the week day name when the component has to occured
        - bysetpos: [int]
            represent the position of the byXXXX sequence relatively to the _freq_
        - wkst: str
            specify the name of the first day of the week
        - datetime_format: bool
            specify if the enddate, if any, has to got a time specified
        """
        if (not freq or freq not in ["SECONDLY", "MINUTELY", "HOURLY", "DAILY", "WEEKLY", "MONTHLY", "YEARLY"]):
            raise Exception(f"Unable to make a recurrent event with an invalid frequence (f{freq})")
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

        self.bysecond = None
        self.byminute = None
        self.byhour = None
        if (datetime_format):
            if (bysecond and any([(value < 0 or value > 60) for value in bysecond])):
                raise Exception(f"There is at least one second value not included between 0 and 60")
            self.bysecond = bysecond
            if (byminute and any([(value < 0 or value > 59) for value in byminute])):
                raise Exception(f"There is at least one minute value not included between 0 and 59")
            self.byminute = byminute
            if (byhour and any([(value < 0 or value > 23) for value in byhour])):
                raise Exception(f"There is at least one hour value not included between 0 and 23")
            self.byhour = byhour

        self.byday = None
        if (byday):
            if (not freq in ["MONTHLY", "YEARLY"]):
                raise Exception(f"Can't add a list of days for not a monthly or yearly frequence")
            if (not all([re.match( "([+-]?([1-9]|[1-4][0-9]|5[0-3]))?(SU|MO|TU|WE|TH|FR|SA)", day) for day in byday])):
                raise Exception(f"Invalid byday expression")
            if (freq == "MONTHLY"):
                for day in byday:
                    tmp = re.search(r"\d+", day)
                    if (tmp and int(tmp.group()) >= 5):
                        raise Exception(f"A month can't have five times the same weekday")
            self.byday = byday

        self.bymonthday = None
        if (bymonthday):
            if (freq == "WEEKLY"):
                raise Exception(f"The BYMONTHDAY rule part MUST NOT be specified when the FREQ rule part is set to WEEKLY")
            if (any([(value < -31 or value > 31 or value == 0) for value in bymonthday])):
                raise Exception(f"BYMONTHDAY valid values are 1 to 31 or -31 to -1")
            self.bymonthday = bymonthday

        self.byyearday = None
        if (byyearday):
            if (freq != "YEARLY"):
                raise Exception(f"The BYYEARDAY rule part MUST NOT be specified when the FREQ rule part is set to DAILY, WEEKLY, or MONTHLY")
            if (any([(value < -366 or value > 366 or value == 0) for value in byyearday])):
                raise Exception(f"BYYEARDAY valid values are 1 to 366 or -366 to -1")
            self.byyearday = byyearday

        self.byweekno = None
        if (byweekno):
            if (freq != "YEARLY"):
                raise Exception(f"The BYWEEKNO rule MUST NOT be used when the FREQ rule part is set to anything other than YEARLY")
            if (any([(value < -53 or value > 53 or value == 0) for value in byyearday])):
                raise Exception(f"BYWEEKNO valid values are 1 to 53 or -53 to -1")
            if (byday and re.search(r"\d+", byday).group()):
                raise Exception(f"the BYDAY rule part MUST NOT be specified with a numeric value with the FREQ rule part set to YEARLY when the BYWEEKNO rule part is specified")
            self.byweekno = byweekno

        self.bymonth = None
        if (bymonth):
            if (any([(value < 1 or value > 12) for value in byyearday])):
                raise Exception(f"BYMONTH valid values are 1 to 12")
            self.bymonth = bymonth

        self.bysetpos = None
        if (bysetpos):
            if ([bysecond, byminute, byhour, byday, bymonthday, byyearday, byweekno, bymonth] == [None]*8):
                raise Exception(f"BYSETPOS rule MUST only be used in conjunction with another BYxxx rule part")
            if (any([(value < -366 or value > 366 or value == 0) for value in byyearday])):
                raise Exception(f"BYSETPOS valid values are 1 to 366 or -366 to -1")
            self.bysetpos = bysetpos

            # not sure if it's my role to implement this, maybe for ICS usage on a real calendar
            # """
            # If multiple BYxxx rule parts are specified, then after evaluating the specified FREQ and INTERVAL rule parts, the BYxxx rule parts are applied to the current set of evaluated occurrences in the following order: BYMONTH, BYWEEKNO, BYYEARDAY, BYMONTHDAY, BYDAY, BYHOUR, BYMINUTE, BYSECOND and BYSETPOS
            # """
            # self.bysetposOwner = None
            # if (self.bymonth):
            #     self.bysetposOwner = "BYMONTH"
            # elif (self.byweekno):
            #     self.bysetposOwner = "BYWEEKNO"
            # elif (self.byyearday):
            #     self.bysetposOwner = "byyearday"
            # elif (self.bymonthday):
            #     self.bysetposOwner = "bymonthday"
            # elif (self.byday):
            #     self.bysetposOwner = "byday"
            # elif (self.byhour):
            #     self.bysetposOwner = "byhour"
            # elif (self.byminute):
            #     self.bysetposOwner = "byminute"
            # elif (self.bysecond):
            #     self.bysetposOwner = "bysecond"

        if (wkst and not wkst in ["SU", "MO", "TU", "WE", "TH", "FR", "SA"]):
            raise Exception(f"Invalid day of the week name ({wkst})")
        self.wkst = wkst


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