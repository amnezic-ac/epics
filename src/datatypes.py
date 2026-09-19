from datetime import datetime

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