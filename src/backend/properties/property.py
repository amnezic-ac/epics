from src.backend.parameters import *
from src.backend.datatypes import *
from src.utils import configuration


class Property():
    pass




class Completed(Property, datetime):
    # have to be specified with UTC Time
    def __init__(self, date_time: datetime):
        self.date_time = date_time

    def __str__(self):
        return f"COMPLETED:{self.date_time.strftime("%Y%m%dT%zZ")}"