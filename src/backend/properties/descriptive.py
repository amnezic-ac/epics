from src.backend.properties.property import *
from src.utils import configuration, logging

class Attachment(Property):
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
        tmp = list(self.categories)
        longueur = len(tmp)

        if (longueur == 0):
            raise Exception(f"Unable to stringify 0 categories")

        result = f"CATEGORIES"
        
        if (self.language):
            result += f";{str(self.language)}"
        
        result += ":"
        for i in range(longueur - 1):
            result += f"{tmp[i]},"
        result += f"{tmp[-1]}"
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
            self.altrep = Altrep(altrep)
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
        self.altrep = Altrep(altrep) if altrep else None
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
        self.altrep = Altrep(altrep) if altrep else None
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
        if (not (value >= 0 and value <= 100)):
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
    def __init__(self, values: [str], altrep: str = None, language: str = None):
        if (not values or values == []):
            values = configuration["resources"]["choices"]
            if (len(values) == 0):
                raise Exception(f"User attempted to create a resource object with no item and no item was found in configuration")
            self.values = set(values)
        self.altrep = Altrep(altrep) if altrep else None
        self.language = Language(language) if language else None

    def add(self, value: str):
        if (not value or not value.strip()):
            logging.warn(f"User tried to add an empty string to a resource object")
        else:
            self.values.add(value.strip())

    def remove(self, value: str):
        if (value == None or not value.strip()):
            logging.warn(f"User tried to remove a non-existing resource")
            raise Exception(f"User tried to remove a non-existing resource")

        value = value.strip()
        if (not value in self.values):
            logging.warn(f"User tried to remove a non-existing resource")
        else:
            self.values.remove(value) 


    def __str__(self):
        result = "RESOURCES"

        if (self.altrep):
            result += f";{str(self.altrep)}"

        if (self.language):
            result += f";{self.language}"

        tmp = list(self.value)
        longueur = len(tmp)
        
        if (longueur == 0):
            raise Exception(f"Can't stringify an empty resource object (this error should not be displayed)")

        result += ":"
        for i in range(longueur - 1):
            result += f"tmp[i],"
        result += f"{tmp[-1]}"

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
        self.altrep = Altrep(altrep) if altrep else None
        
        try:
            self.language = Language(language) if language else None
        except Exception as e:
            raise Exception(f"{self.value} title language: {e}")

    def __str__(self):
        result = "SUMMARY"

        if (self.altrep):
            result += f";{str(self.altrep)}"

        if (self.language):
            result += f";{str(self.language)}"

        result += f":{self.value}"
        return result