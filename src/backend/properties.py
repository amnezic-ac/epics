# section 3.8.1

from src.backend.parameters import *
from src.backend.datatypes import *

DEFAULT_DURATION_HOUR = 2

class Property():
    pass

class Uid(Property):
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f"UID:{self.value}"

class Attachement(Property):
    # not displayed on thunderbird
    
    # now (sub)typename is considered always valid, need work on that
    def __init__(self, value: str, encoding: str = None, typename: str = None, subtypename: str = None):
        self.value = value
        self.encoding = encoding
        self.fmttype = None
        if (typename and subtypename):
            self.fmttype = Fmttype(typename, subtypename)

    def __str__(self):
        result = "ATTACH"

        if (self.fmttype):
            result += f";{str(self.fmttype)}"

        if (self.encoding):
            result += f";ENCODING={self.encoding.upper()};VALUE=BINARY"
        
        result += f":{self.value}"
        return result

class Categories(Property):
    # on considère que la langue donnée est correcte
    def __init__(self, categories: [str], language : str = None):
        self.categories = set(categories)
        self.language = language # needs to comply with RFC 5646

    def add_category(category : str):
        self.categories.add(category)

    def remove_category(category: str) -> bool:
        self.categories.remove(category)


    def __str__(self):
        result = f"CATEGORIES"

        if (self.language):
            result += f";LANGUAGE={self.language}"

        tmp = list(self.categories)
        result += f":{tmp[0]}"
        tmp.pop(0)

        for category in tmp:
            result += f",{category}"

        return result

class Classification(Property):
    # not displayed on thunderbird (for event)

    def __init__(self, value: str = "PUBLIC"):
        self.value = str.upper(value)
        # possible values of Class are: Public, Private and Confidential

    def __str__(self):
        return f"CLASS:{self.value}"

class Comment(Property):

    def __init__(self, value: str, altrep: str = None, language: str = None):
        self.value = value
        self.altrep = None
        if (altrep):
            self.altrep = Altrep(altrep, value)
        self.language = None
        if (language):
            self.language = Language(language)

    def __str__(self):
        result = f"COMMENT"

        if (self.altrep):
            result += f";{str(self.altrep)}"

        if (self.language):
            result += f";{str(self.language)}"

        result += f":{self.value}"
        return result

class Description(Property):
    
    def __init__(self, value: str, altrep: str = None, language: str = None):
        self.value = value
        self.altrep = Altrep(altrep, value) if altrep else None
        self.language = Language(language) if language else None

    def __str__(self):
        result = "DESCRIPTION"

        if (self.altrep):
            result += f";{str(self.altrep)}"

        if (self.language):
            result += f";{str(self.language)}"

        result += f":{self.value}"
        return result

class Geo(Property):
    # not displayed on thunderbird (for event)

    def __init__(self, latitude: float, longitude: float):
        if (not (latitude >= -90 and latitude <= 90)):
            raise Exception(f"Invalid latitude value ({self.latitude}), should be between -90 and 90")
        if (not (longitude >= -180 and longitude <= 180)):
            raise Exception(f"Invalid latitude value ({self.latitude}), should be between -90 and 90")

        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"GEO:{str(self.latitude)};{str(self.longitude)}"
            
class Location(Property):

    def __init__(self, value: str, altrep: str = None, language: str = None):
        self.value = value
        self.altrep = Altrep(altrep, value) if altrep else None
        self.language = Language(language) if language else None

    def __str__(self):
        result = "LOCATION"

        if (self.altrep):
            result += f";{str(self.altrep)}"

        if (self.language):
            result += f";{str(self.language)}"

        result += f":{self.value}"
        return result

class Percent(Property):

    def __init__(self, value: int):
        if (not (self.value >= 0 and self.value <= 100)):
            raise Exception(f"Percentage have to be between 0 and 100 (current value: {self.value})")
        self.value = value

        def __str__(self):
            return f"PERCENT-COMPLETE:{self.value}"

class Priority(Property):
    # not displayed on thunderbird (for event)
    def __init__(self, value: int = 0):
        if (value < 0 or value > 9):
            raise Exception(f"Priority value have to be include between 0 and 9")

        self.value = value

    def __str__(self):
        return f"PRIORITY:{self.value}"

class Resources(Property):
    def __init__(self, value: str, altrep: str = None, language: str = None):
        self.value = value
        self.altrep = Altrep(altrep, value) if altrep else None
        self.language = Language(language) if language else None

    def __str__(self):
        result = "RESOURCES"

        if (self.altrep):
            result += f";{str(self.altrep)}"

        if (self.language):
            result += f";{self.language}"

        result += f":{self.value}"
        return result

class Status(Property):
    # not displayed on thunderbird
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f"STATUS:{self.value}"

class Summary(Property):
    def __init__(self, value: str, altrep: str = None, language: str = None):
        self.value = value
        self.altrep = Altrep(altrep, value) if altrep else None
        self.language = Language(language) if language else None

    def __str__(self):
        result = "SUMMARY"

        if (self.altrep):
            result += f";{str(self.altrep)}"

        if (self.language):
            result += f";{str(self.language)}"

        result += f":{self.value}"
        return result

class Completed(Property, datetime):
    # have to be specified with UTC Time
    def __init__(self, date_time: datetime):
        self.date_time = date_time

    def __str__(self):
        return f"COMPLETED:{self.date_time.strftime("%Y%m%dT%zZ")}"

class Duration(Property):
    def __init__(self, week: int = 0, day: int = 0, hour: int = DEFAULT_DURATION_HOUR, minute: int = 0, second: int = 0):
        self.value = DurationType(week, day, hour, minute, second)

    def __str__(self):
        return f"DURATION:{str(self.value)}"

class Freebusytime(Property):
    def __init__(self, status: str = "BUSY", week: int = 0, day: int = 0, hour: int = DEFAULT_DURATION_HOUR, minute: int = 0, second: int = 0):
        self.value = Duration(week, day, hour, minute, second)
        self.status = Fbtype(status)

    def __str__(self):
        return f"DURATION;{str(self.status)}:{str(self.value)}"

class Transparency(Property):
    # not displayed on thunderbird
    def __init__(self, value: str = "OPAQUE"):
        if (value not in ["OPAQUE", "TRANSPARENT"]):
            raise Exception(f"Transparency property can only take OPAQUE o TRANSPARENT value, actual value: {value}")

        self.value = value

    def __str__(self):
        return f"TRANSP:{self.value}"
        
class Atttendee(Property):
    # un peu plus complexe que ça (3.8.4.1)

    def __init__(self, name: str, cutypeparam: str = None, memberparam: str = None, roleparam: str = None, parstatparam: str = None, rsvpparam: bool = None, deltoparam: str = None, delfromparam: str = None, sentbyparam: str = None, cnparam: str = None, dirparam: str = None, languageparam: str = None):
        if (not name):
            raise Exception(f"Attendee name can't be None")

        self.name = name

        self.cutypeparam = Cutype(cutypeparam) if cutypeparam else None
        self.memberparam = Member(memberparam) if memberparam else None
        self.roleparam = Role(roleparam) if roleparam else None
        self.partstatparam = Partstat(parstatparam) if parstatparam else None
        self.rsvpparam = Rsvp(rsvpparam) if rsvpparam != None else None
        # the following attributes have to be Caladress
        self.deltoparam = Delto(deltoparam) if deltoparam else None
        self.delfromparam = Delfrom(delfromparam) if delfromparam else None
        self.sentbyparam = Sentby(sentbyparam) if sentbyparam else None
        ########
        self.cnparam = Cn(cnparam) if cnparam else None
        self.dirparam = Dir(dirparam) if dirparam else None
        self.languageparam = Language(languageparam) if languageparam else None

    def __str__(self):
        result = "ATTENDEE"

        if (self.cutypeparam):
            result += f";{str(self.cutypeparam)}"
        if (self.memberparam):
            result += f";{str(self.memberparam)}"
        if (self.roleparam):
            result += f";{str(self.roleparam)}"
        if (self.partstatparam):
            result += f";{str(self.partstatparam)}"
        if (self.rsvpparam):
            result += f";{str(self.rsvpparam).upper()}"
        if (self.deltoparam):
            result += f";{str(self.deltoparam)}"
        if (self.delfromparam):
            result += f";{str(self.delfromparam)}"
        if (self.sentbyparam):
            result += f";{str(self.sentbyparam)}"
        if (self.cnparam):
            result += f";{str(self.cnparam)}"
        if (self.dirparam):
            result += f";{str(self.dirparam)}"
        if (self.languageparam):
            result += f";{str(self.languageparam)}"

        result += f":{self.name}"
        
        return result

class Contact(Property):
    # not displayed on thunderbird
    def __init__(self, value: str, altrep: str = None, language: str = None):
        if (not value):
            raise Exception (f"Contact value can't be None")

        self.value = value
        self.altrep = Altrep(altrep, value) if altrep else None
        self.language = Language(language) if language else None

    def __str__(self):
        result = "CONTACT"

        if (self.altrep):
            result += f";{str(self.altrep)}"
        if (self.language):
            result += f";{str(self.language)}"

        result += f":{self.value}"
        return result

class Organizer(Property):
    def __init__(self, value: str, cnparam: str = None, dirparam: str = None, sentbyparam: str = None, languageparam: str = None):
        if (not value):
            raise Exception(f"Organizer value can't be None")

        self.value = value
        self.cnparam = Cn(cnparam) if cnparam else None
        self.dirparam = Dir(dirparam) if dirparam else None
        self.sentbyparam = Sentby(sentbyparam) if sentbyparam else None
        self.languageparam = Language(languageparam) if languageparam else None

    def __str__(self):
        result = "Organizer"

        if (self.cnparam):
            result += f";{str(self.cnparam)}"
        if (self.dirparam):
            result += f";{str(self.dirparam)}"
        if (self.sentbyparam):
            result += f";{str(self.sentbyparam)}"
        if (self.languageparam):
            result += f";{str(self.languageparam)}"

        result += f":{self.value}"
        return result